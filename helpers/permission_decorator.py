from django.shortcuts import redirect
from django.urls import reverse


def business_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to the business login page
            return redirect(reverse("business-login"))
        return view_func(request, *args, **kwargs)

    return _wrapped_view
