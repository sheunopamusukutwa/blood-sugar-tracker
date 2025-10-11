# tracker/views.py

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

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
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(APIView):
    """
    Obtain an auth token using username/password.
    POST: { "username": "...", "password": "..." } -> { "token": "..." }
    """
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
# Filtering & Ordering
# ---------------------------

class ReadingFilter(df.FilterSet):
    """
    Supported query params on /api/readings/:
      - ?date_from=YYYY-MM-DD  (inclusive)
      - ?date_to=YYYY-MM-DD    (inclusive)
      - ?status=fasting|random|postprandial  (case-insensitive)
      - ?ordering=timestamp|-timestamp|value|-value|status|-status
    """
    # Filter against the DATE part of the timestamp (works with DateTimeField)
    date_from = df.DateFilter(field_name="timestamp__date", lookup_expr="gte")
    date_to = df.DateFilter(field_name="timestamp__date", lookup_expr="lte")

    # Case-insensitive exact match on status; adjust if you use choices.
    status = df.CharFilter(field_name="status", lookup_expr="iexact")

    class Meta:
        model = Reading
        fields = ["date_from", "date_to", "status"]


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
    ordering_fields = ["timestamp", "value", "status"]
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
