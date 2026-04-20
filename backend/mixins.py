from django.contrib.auth.mixins import UserPassesTestMixin


class AdminRequiredMixin(UserPassesTestMixin):
    """restricts access to users with the admin role."""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin


class AdminOrTrainerMixin(UserPassesTestMixin):
    """restricts access to admin and trainer roles."""

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_admin or self.request.user.is_trainer
        )
