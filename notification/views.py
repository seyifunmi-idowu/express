from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from feleexpress.middlewares.permissions.is_authenticated import IsAuthenticated
from helpers.utils import ResponseManager
from notification.docs import schema_doc
from notification.serializers import NotificationSerializer
from notification.service import NotificationService


class NotificationViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Get all user notification",
        operation_summary="Get all user notification",
        tags=["Notification"],
        responses=schema_doc.GET_USER_NOTIFICATION_RESPONSE,
    )
    def list(self, request):
        notifications = NotificationService.get_user_notifications(request.user)
        return ResponseManager.handle_response(
            data=NotificationSerializer(notifications, many=True).data,
            status=status.HTTP_200_OK,
            message="User notifications",
        )

    @swagger_auto_schema(
        methods=["post"],
        operation_description="User read notification",
        operation_summary="User read notification",
        tags=["Notification"],
        responses=schema_doc.OPENED_USER_NOTIFICATION_RESPONSE,
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="(?P<notification_id>[a-z,A-Z,0-9]+)/opened",
    )
    def opened_notification(self, request, notification_id):
        response = NotificationService.opened_notification(
            notification_id, request.user
        )
        return ResponseManager.handle_response(
            data=response, status=status.HTTP_200_OK, message="success"
        )
