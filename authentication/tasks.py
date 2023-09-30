from celery import shared_task

from authentication.models import User


# @shared_task(name="task.track_user_activity")
def track_user_activity(
    context,
    category,
    action,
    email=None,
    phone_number=None,
    user_type="CUSTOMER",
    level="INFO",
    target_user_id=None,
    target_user_type="CUSTOMER",
    session_id=None,
):
    if not email and not phone_number:
        return None  # probably raise an error here

    from authentication.service import UserActivityService
    from customer.service import CustomerService
    from rider.service import RiderService

    if email:
        user = User.objects.filter(email=email).first()
    else:
        user = User.objects.filter(phone_number=phone_number).first()
    customer, rider = None, None
    if user_type == "CUSTOMER":
        customer = CustomerService.get_customer(user=user)
    else:
        rider = RiderService.get_rider(user=user)
    if target_user_id:
        target_user = User.objects.filter(id=target_user_id).first()
        if target_user_type == "CUSTOMER":
            customer = CustomerService.get_customer(user=target_user)
        else:
            rider = RiderService.get_rider(user=target_user)

    UserActivityService.capture_activity(
        user=user,
        customer=customer,
        rider=rider,
        context=context,
        category=category,
        action=action,
        level=level,
        session_id=session_id,
    )
