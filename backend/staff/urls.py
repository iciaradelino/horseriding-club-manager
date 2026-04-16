from django.urls import path
from . import views

app_name = "staff"

urlpatterns = [
    path("", views.TrainerListView.as_view(), name="list"),
    path("<int:pk>/", views.TrainerDetailView.as_view(), name="detail"),
    path("add/", views.TrainerCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.TrainerUpdateView.as_view(), name="update"),
]
