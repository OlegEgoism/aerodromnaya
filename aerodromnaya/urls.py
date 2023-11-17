"""
URL configuration for aerodromnaya project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from aerodromnaya import settings
from partnership import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.info, name='info'),
    path('feedback_job_create/', views.feedback_job_create, name='feedback_job_create'),
    path('feedback_send/', views.feedback_send, name='feedback_send'),
    path('feedback_send_limit/', views.feedback_send_limit, name='feedback_send_limit'),
    path('feedback_jobs_status_in_work/', views.feedback_jobs_status_in_work, name='feedback_jobs_status_in_work'),
    path('feedback_jobs_status_completed/', views.feedback_jobs_status_completed, name='feedback_jobs_status_completed'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
