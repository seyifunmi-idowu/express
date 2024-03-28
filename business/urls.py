from django.urls import path

import business.views as views

urlpatterns = [
    path("login", views.signin, name="business-login"),
    path("logout", views.sign_out, name="business-logout"),
    path("register", views.register, name="business-register"),
    path("verify/email", views.verify_email, name="business-verify-email"),
    path("register/resend-otp", views.resend_otp, name="resend-otp"),
    path("dashboard", views.dashboard, name="business-dashboard"),
    path("settings", views.settings, name="business-settings"),
    path(
        "regenerate-secret-key",
        views.regenerate_secret_key,
        name="business-regenerate-secret-key",
    ),
    # API DOCS
    path("api/docs", views.docs_index, name="business-api-docs"),
]
