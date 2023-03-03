import logging

from django.conf import settings
from nautobot.users.models import User
from django.contrib.auth.backends import ModelBackend

from tacacs_plus.client import TACACSClient
from tacacs_plus.flags import TAC_PLUS_AUTHEN_TYPES

logger = logging.getLogger(__name__)


# nautobot_config.py:
#
# TACACS+ settings (default host to empty string to skip using TACACS+ auth).
# Note: These settings may be overridden by database settings.
# TACACSPLUS_HOST = 'tacacs_host'
# TACACSPLUS_PORT = 49
# TACACSPLUS_SECRET = 'tacacs_secret'
# TACACSPLUS_SESSION_TIMEOUT = 5
# TACACSPLUS_AUTH_PROTOCOL = 'pap'
# TACACSPLUS_AUTOCREATE_USERS = True
#
# AUTHENTICATION_BACKENDS = [
#     'django_auth_tacacs.nautobot.TACACSPlusAuthenticationBackend',
#     'nautobot.core.authentication.ObjectPermissionBackend',
# ]


class TACACSPlusAuthenticationBackend(ModelBackend):
    """Authenticate via TACACS+

    Authorization is not implemented, only login authentication
    """

    def _get_or_set_user(self, username, password, create_user=False):
        if create_user:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"is_superuser": False, "is_staff": False},
            )
            if created:
                logger.debug("Created TACACS+ user %s" % (username,))
        else:
            try:
                user = User.objects.get(username=username)
                logger.debug("user authenticated via Tacacs+ backend")
            except User.DoesNotExist:
                return None
        return user

    def authenticate(self, request, username, password):
        if not settings.TACACSPLUS_HOST:
            return None
        try:
            # Upstream TACACS+ client does not accept non-string, so convert if needed.
            auth = TACACSClient(
                settings.TACACSPLUS_HOST,
                settings.TACACSPLUS_PORT,
                settings.TACACSPLUS_SECRET,
                timeout=settings.TACACSPLUS_SESSION_TIMEOUT,
            ).authenticate(
                username,
                password,
                authen_type=TAC_PLUS_AUTHEN_TYPES[settings.TACACSPLUS_AUTH_PROTOCOL],
            )
        except Exception as e:
            logger.exception("TACACS+ Authentication Error: %s" % str(e))
            return None
        if auth.valid:
            return self._get_or_set_user(
                username, password, settings.TACACSPLUS_AUTOCREATE_USERS
            )

    def get_user(self, user_id):
        if not settings.TACACSPLUS_HOST:
            return None
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
