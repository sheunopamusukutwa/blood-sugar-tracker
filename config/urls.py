"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def root_view(_request):
    return JsonResponse({
        "name": "Blood Sugar Tracker API",
        "health": "/healthz",
        "endpoints": {
            "register": "/api/register/",
            "login": "/api/login/",
            "profile": "/api/profile/",
            "readings_list_create": "/api/readings/",
            "reading_detail": "/api/readings/{id}/"
        }
    })

def healthz(_request):
    return JsonResponse({"status": "ok"})

def api_index(_request):
    return JsonResponse({
        "name": "Blood Sugar Tracker API",
        "version": 1,
        "health": "/healthz",
        "endpoints": {
            "register": "/api/register/",
            "login": "/api/login/",
            "profile": "/api/profile/",
            "readings_list_create": "/api/readings/",
            "reading_detail": "/api/readings/{id}/",
            "filter_by_notes": "/api/readings/?notes_icontains=after%20dinner",
            "filter_by_date": "/api/readings/?timestamp_after=2025-10-18T00:00:00Z&timestamp_before=2025-10-19T00:00:00Z",
            "ordering": "/api/readings/?ordering=-timestamp"
        }
    })

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", root_view),                 # GET / → small JSON landing
    path("healthz", healthz),            # GET /healthz → {"status":"ok"}
    path("api/", api_index, name="api-index"),
    # Mount all tracker routes under /api/
    path("api/", include("tracker.urls")),
]
