from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),

    # Admin-only user management UI
    path("users/",                       views.UserListView.as_view(),          name="user_list"),
    path("users/<int:pk>/",              views.UserDetailView.as_view(),        name="user_detail"),
    path("users/<int:pk>/edit/",         views.UserUpdateView.as_view(),        name="user_update"),
    path("users/<int:pk>/password/",     views.UserPasswordResetView.as_view(), name="user_password"),
    path("users/<int:pk>/delete/",       views.UserDeleteView.as_view(),        name="user_delete"),
]
