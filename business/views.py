from django.contrib import messages
from django.contrib.auth import logout
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.urls import reverse

from authentication.service import AuthService, UserService
from business.forms import (
    BusinessRegistrationForm,
    FundWalletForm,
    LoginForm,
    SubmitWebhookUrlForm,
    VerifyEmailForm,
)
from business.service import BusinessAuth, BusinessService
from helpers.db_helpers import generate_session_id
from helpers.permission_decorator import business_login_required
from helpers.validators import CustomAPIException
from wallet.service import CardService


def signin(request):
    if request.user.is_authenticated and request.user.user_type == "BUSINESS":
        return redirect(reverse("business-dashboard"))

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            response = BusinessAuth.login_business_user(
                request, form.cleaned_data, generate_session_id()
            )
            if response:
                return redirect(reverse("business-dashboard"))
    else:
        form = LoginForm()

    context = {"form": form}
    return render(request, "app/login.html", context)


def verify_email(request):
    email = request.GET.get("email", "")
    if request.method == "POST":
        form = VerifyEmailForm(request.POST)
        if form.is_valid():
            BusinessAuth.verify_business_user_email(
                request, form.cleaned_data, generate_session_id()
            )
            return redirect(reverse("business-dashboard"))

    else:
        form = VerifyEmailForm()
    context = {"form": form, "email": email}
    return render(request, "app/verify_email.html", context)


def register(request):
    """ Add a new user """

    if request.user.is_authenticated and request.user.user_type == "BUSINESS":
        return redirect(reverse("business-dashboard"))

    if request.method == "POST":
        form = BusinessRegistrationForm(request.POST)

        if form.is_valid():
            BusinessAuth.register_business_user(
                form.cleaned_data, generate_session_id()
            )
            return redirect(
                reverse("business-verify-email")
                + f"?email={form.cleaned_data.get('email')}"
            )
    else:
        form = BusinessRegistrationForm()
    return render(request, "app/signup.html", {"form": form})


def resend_otp(request):
    email = request.GET.get("email", "")
    user = UserService.get_user_instance(email=email)
    if user is None:
        messages.add_message(request, messages.ERROR, "User not found.")
    else:
        AuthService.initiate_email_verification(email=email, name=user.display_name)
    return redirect(reverse("business-verify-email") + f"?email={email}")


@business_login_required
def sign_out(request):
    logout(request)
    return redirect(reverse("business-login"))


@business_login_required
def dashboard(request):
    response = BusinessAuth.get_business_dashboard_view(request.user)
    context = {"view": "Dashboard", **response}
    return render(request, "app/dashboard.html", context)


@business_login_required
def order(request):
    response = BusinessAuth.get_business_order_view(request.user)
    context = {"view": "Order", **response}
    return render(request, "app/order.html", context)


@business_login_required
def view_order(request, order_id):
    response = BusinessAuth.get_business_retrieve_order_view(request.user, order_id)
    context = {"view": "Order", **response}
    return render(request, "app/view_order.html", context)


@business_login_required
def wallet(request):
    response = BusinessAuth.get_business_wallet_view(request.user)
    transactions = response.pop("transactions", [])

    paginator = Paginator(transactions, 10)
    page_number = request.GET.get("page")
    try:
        transactions = paginator.page(page_number)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    context = {"view": "Wallet", "transactions": transactions, **response}
    return render(request, "app/wallet.html", context)


@business_login_required
def regenerate_secret_key(request):
    BusinessAuth.regenerate_secret_key(request.user, generate_session_id())
    return redirect(reverse("business-settings"))


@business_login_required
def settings(request):
    if request.method == "POST":
        form = SubmitWebhookUrlForm(request.POST)
        if form.is_valid():
            BusinessService.update_webhook(
                request.user, form.cleaned_data, generate_session_id()
            )
    else:
        form = SubmitWebhookUrlForm()

    business = BusinessService.get_business(user=request.user)
    secret_key = BusinessService.get_business_user_secret_key(user=request.user)
    context = {
        "view": "Settings",
        "form": form,
        "secret_key": secret_key,
        "current_webhook_url": business.webhook_url,
    }
    return render(request, "app/settings.html", context)


@business_login_required
def fund_wallet(request):
    if request.method == "POST":
        form = FundWalletForm(request.POST)
        if form.is_valid():
            callback_url = request.build_absolute_uri(
                reverse("business-verify-card-transaction")
            )
            response_url = BusinessService.initiate_transaction(
                request.user,
                form.cleaned_data.get("amount"),
                generate_session_id(),
                callback_url,
            )
            return redirect(response_url)

    return redirect(reverse("business-wallet"))


def verify_business_card_transaction(request):
    try:
        CardService.verify_card_transaction(request.GET)
    except CustomAPIException as e:
        messages.add_message(request, messages.ERROR, e)
    return redirect(reverse("business-wallet"))


@business_login_required
def delete_card(request, card_id):
    card = CardService.get_user_cards(id=card_id, user=request.user).first()
    if card:
        card.delete()
    return redirect(reverse("business-wallet"))


@business_login_required
def docs_index(request):
    context = {"base_url": "api.feleexpress.com"}
    return render(request, "docs/index.html", context)
