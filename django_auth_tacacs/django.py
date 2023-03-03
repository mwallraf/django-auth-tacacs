import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

from tacacs_plus.client import TACACSClient
from tacacs_plus.flags import TAC_PLUS_AUTHEN_TYPES

logger = logging.getLogger(__name__)


#
# settings.py
# TACACSPLUS_HOST = 'localhost'
# TACACSPLUS_PORT = 49
# TACACSPLUS_SECRET = 'super-secret'
# TACACSPLUS_SESSION_TIMEOUT = 5
# TACACSPLUS_AUTH_PROTOCOL = 'ascii'
# TACACSPLUS_AUTOCREATE_USERS = False
#
# AUTHENTICATION_BACKENDS = [
#     'django_auth_tacacs.django.TACACSPlusAuthenticationBackend',
#     'django.contrib.auth.backends.ModelBackend',
# ]
#

class TACACSPlusAuthenticationBackend(ModelBackend):
    """Authenticate via TACACS+

    Authorization is not implemented, only login authentication
    """

    def _get_or_set_user(self, username, password, create_user=False):

        if create_user:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'is_superuser': False, 'is_staff': False},
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
            ).authenticate(username, password, authen_type=TAC_PLUS_AUTHEN_TYPES[settings.TACACSPLUS_AUTH_PROTOCOL])
        except Exception as e:
            logger.exception("TACACS+ Authentication Error: %s" % str(e))
            return None
        if auth.valid:
            return self._get_or_set_user(username, password, settings.TACACSPLUS_AUTOCREATE_USERS)

    def get_user(self, user_id):
        if not settings.TACACSPLUS_HOST:
            return None
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
