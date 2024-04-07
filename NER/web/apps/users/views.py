from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from .models import InviteCode

import uuid

from django.views.generic import DetailView, RedirectView, UpdateView

User = get_user_model()


class GenerateInviteCodeView(LoginRequiredMixin, CreateView):
    model = InviteCode
    fields = []  # No fields are needed from the user in the form
    template_name = 'users/generate_invite_code.html'
    success_url = reverse_lazy('where_to_redirect_after_creation')  # Adjust this

    def form_valid(self, form):
        form.instance.code = str(uuid.uuid4())[:8]
        form.instance.creator = self.request.user  # Set the creator as the current user
        return super().form_valid(form)

generate_invite_view = GenerateInviteCodeView.as_view()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self, queryset=None):
        # Return the current user
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming every user has a NewsletterPreference object
        return context


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail")


user_redirect_view = UserRedirectView.as_view()
