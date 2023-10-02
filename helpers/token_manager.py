from typing import Dict, Optional, Type

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, BlacklistMixin, RefreshToken

from authentication.models import User


class CustomAccessToken(BlacklistMixin, AccessToken):
    pass


class TokenManager:
    @classmethod
    def prepare_user_token(cls, user: Type[User], session_id: str = None) -> Dict:
        from authentication.tasks import track_user_activity

        token = RefreshToken.for_user(user)
        track_user_activity(
            context={},
            category="USER_LOGIN_ATTEMPT",
            action="USER_LOGIN_ATTEMPT_SUCCESS_WITH_TOKEN",
            email=user.email if user.email else None,
            phone_number=user.phone_number if user.phone_number else None,
            level="SUCCESS",
            session_id=session_id,
        )
        return {"refresh": str(token), "access": str(token.access_token)}

    @classmethod
    def logout(cls, access_token: Optional[str]) -> None:
        try:
            token = CustomAccessToken(access_token)
            token.blacklist()
        except TokenError:
            # TODO: Log this exception to Sentry but don't raise it
            pass
