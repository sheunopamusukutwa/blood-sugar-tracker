# tracker/views.py

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.http import JsonResponse

from rest_framework import generics, permissions, status, filters as drf_filters
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

import django_filters as df
from django_filters.rest_framework import DjangoFilterBackend

from .models import Reading
from .serializers import RegisterSerializer, UserSerializer, ReadingSerializer


# ---------------------------
# Auth & Profile
# ---------------------------

class RegisterView(generics.CreateAPIView):
    """
    Register a new user.
    POST: { "username": "...", "email": "...", "password": "..." }
    RESP: { "message": "User registered successfully" }
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # explicitly open

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # RegisterSerializer.create() hashes password
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class LoginView(APIView):
    """
    Obtain a DRF auth token using username/password.
    POST: { "username": "...", "password": "..." } -> { "token": "..." }
    Use header on protected routes: Authorization: Token <token>
    """
    permission_classes = [permissions.AllowAny]  # explicitly open

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    """
    Get/Update the authenticated user's profile.
    GET -> user data
    PUT (partial) -> update username/email
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------
# Health & API Index
# ---------------------------

class HealthCheckView(APIView):
    """
    Lightweight health check for uptime monitors.
    GET -> {"status":"ok"}
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class ApiIndexView(APIView):
    """
    Simple root index so hitting "/" returns something useful in prod.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(
            {
                "name": "Blood Sugar Tracker API",
                "version": "v1",
                "endpoints": {
                    "register": "/api/register/",
                    "login": "/api/login/",
                    "profile": "/api/profile/",
                    "readings": "/api/readings/",
                    "health": "/healthz",
                },
            },
            status=status.HTTP_200_OK,
        )


# ---------------------------
# Filtering & Ordering
# ---------------------------

class ReadingFilter(df.FilterSet):
    """
    Supported query params on /api/readings/:
      - ?date_from=YYYY-MM-DD  (inclusive)
      - ?date_to=YYYY-MM-DD    (inclusive)
      - ?notes=after dinner    (case-insensitive exact)
      - ?notes_icontains=dinner   (substring match, case-insensitive)
      - ?ordering=timestamp|-timestamp|value|-value|notes|-notes
    """
    # Filter against the DATE part of the timestamp (works with DateTimeField)
    date_from = df.DateFilter(field_name="timestamp__date", lookup_expr="gte")
    date_to = df.DateFilter(field_name="timestamp__date", lookup_expr="lte")

    # Case-insensitive exact match on notes; icontains available via explicit lookup
    notes = df.CharFilter(field_name="notes", lookup_expr="iexact")
    notes_icontains = df.CharFilter(field_name="notes", lookup_expr="icontains")

    class Meta:
        model = Reading
        # We explicitly define which filters are allowed via the attributes above
        fields = ["date_from", "date_to", "notes", "notes_icontains"]


# ---------------------------
# Readings CRUD
# ---------------------------

class ReadingListCreateView(generics.ListCreateAPIView):
    """
    List & create readings for the authenticated user.
    Filtering + ordering enabled via query params (see ReadingFilter).
    """
    serializer_class = ReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Enable django-filter + DRF ordering
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter]
    filterset_class = ReadingFilter

    # Allow clients to order by these fields. Default is newest first.
    ordering_fields = ["timestamp", "value", "notes"]
    ordering = ["-timestamp"]

    def get_queryset(self):
        # Default ordering applied; OrderingFilter can override via ?ordering=
        return Reading.objects.filter(user=self.request.user).order_by("-timestamp")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReadingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve/Update/Delete a single reading (owned by the authenticated user).
    """
    serializer_class = ReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reading.objects.filter(user=self.request.user)