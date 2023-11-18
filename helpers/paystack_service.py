import requests
from django.conf import settings


class PaystackService:

    secret_key = settings.PAYSTACK_SECRET_KEY
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }
    base_url = "https://api.paystack.co/"

    @classmethod
    def verify_account_number(cls, bank_code, account_number):
        url = f"{cls.base_url}bank/resolve?account_number={account_number}&bank_code={bank_code}"
        response = requests.get(url, headers=cls.headers)
        return response.json()

    @classmethod
    def get_banks(cls):
        url = f"{cls.base_url}bank"
        response = requests.get(url, headers=cls.headers)
        # TODO: for optimization, save and retrieve in a cache
        return cls.format_list_of_banks(response.json()["data"])

    @classmethod
    def create_transfer_recipient(cls, name, bank_code, account_number):
        data = {
            "type": "nuban",
            "name": name,
            "account_number": account_number,
            "bank_code": bank_code,
            "currency": "NGN",
        }
        url = f"{cls.base_url}transferrecipient"
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()

    @classmethod
    def initiate_transfer(cls, amount, recipient):
        data = {
            "source": "balance",
            "amount": amount,
            "recipient": recipient,
            "reason": "payment from fele",
        }
        url = f"{cls.base_url}transfer"
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()

    @classmethod
    def create_payment_page(cls, data):
        url = f"{cls.base_url}page"
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()

    @classmethod
    def verify_transaction(cls, reference):
        url = f"{cls.base_url}transaction/verify/{reference}"
        response = requests.get(url, headers=cls.headers)
        return response.json()

    @classmethod
    def initialize_payment(cls, email, amount, currency="NGN", callback_url=None):
        data = {
            "email": email,
            "amount": amount * 100,
            "currency": currency,
            "callback_url": callback_url,
        }
        url = f"{cls.base_url}transaction/initialize"
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()

    @classmethod
    def charge_card(cls, email, amount, card_auth):
        amount = round(float(amount) * 100)
        data = {"email": email, "amount": amount, "authorization_code": card_auth}
        url = f"{cls.base_url}transaction/charge_authorization"
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()

    @staticmethod
    def format_list_of_banks(banks_data):
        formatted_banks = [
            {"name": bank["name"], "code": bank["code"]} for bank in banks_data
        ]
        return formatted_banks
