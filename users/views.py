from django.http import Http404
from django.shortcuts import redirect
from .models import User
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import UserRegisterForm


def verify(request, uuid):
    """verification users"""
    try:
        user = User.objects.get(
            verification_uuid=uuid,
            is_verified=False
        )
    except User.DoesNotExist:
        raise Http404("User does not exist or is already verified")

    user.is_verified = True
    user.save()

    return redirect('users:login')


class UserRegisterView(FormView):
    """User registration view"""

    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
