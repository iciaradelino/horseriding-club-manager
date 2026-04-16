from django.urls import path
from . import views

app_name = "lessons"

urlpatterns = [
    path("", views.LessonListView.as_view(), name="list"),
    path("<int:pk>/", views.LessonDetailView.as_view(), name="detail"),
    path("add/", views.LessonCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.LessonUpdateView.as_view(), name="update"),
]
