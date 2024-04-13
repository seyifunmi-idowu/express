from django.urls import path

import business.views as views

urlpatterns = [
    path("login", views.signin, name="business-login"),
    path("logout", views.sign_out, name="business-logout"),
    path("register", views.register, name="business-register"),
    path("verify/email", views.verify_email, name="business-verify-email"),
    path("register/resend-otp", views.resend_otp, name="resend-otp"),
    path("dashboard", views.dashboard, name="business-dashboard"),
    path("order", views.order, name="business-order"),
    path("order/<str:order_id>", views.view_order, name="business-view-order"),
    path("wallet", views.wallet, name="business-wallet"),
    path(
        "paystack/callback",
        views.verify_business_card_transaction,
        name="business-verify-card-transaction",
    ),
    path("settings", views.settings, name="business-settings"),
    path("fund-wallet", views.fund_wallet, name="business-fund-wallet"),
    path("delete/card/<str:card_id>", views.delete_card, name="business-delete-card"),
    path(
        "regenerate-secret-key",
        views.regenerate_secret_key,
        name="business-regenerate-secret-key",
    ),
    # API DOCS
    path("api/docs", views.docs_index, name="business-api-docs"),
]
