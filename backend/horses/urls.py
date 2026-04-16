from django.urls import path
from . import views

app_name = "horses"

urlpatterns = [
    path("", views.HorseListView.as_view(), name="list"),
    path("<int:pk>/", views.HorseDetailView.as_view(), name="detail"),
    path("add/", views.HorseCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.HorseUpdateView.as_view(), name="update"),
    path("<int:horse_pk>/health/add/", views.HealthRecordCreateView.as_view(), name="health_record_create"),
]
