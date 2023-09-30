from customer.models import Customer
from helpers.db_helpers import select_for_update


class CustomerService:
    @classmethod
    def get_customer(cls, **kwargs) -> Customer:
        """Get a customer instance"""
        return Customer.objects.filter(**kwargs).first()

    @classmethod
    def get_and_lock_customer(cls, **kwargs):
        """
        Get customer and lock down that customer instance until the
        transaction is complete. This method should only be
        called in an atomic block
        """
        return select_for_update(Customer, **kwargs)

    @classmethod
    def list_customer(cls, **kwargs):
        """List customers"""
        return Customer.objects.filter(**kwargs)

    @classmethod
    def update_customer(cls, customer: Customer, **kwargs) -> Customer:
        """A service method that updates a Customer's data"""
        for field, value in kwargs.items():
            setattr(customer, field, value)
        customer.save(update_fields=kwargs.keys())
        return customer
