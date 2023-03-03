# django-auth-tacacs

A django authentication backend that uses Tacacs+ for authentication. This can also be used with Nautobot or Netbox.

## Description

This backend authenticates users via Tacacs+. Only authentication is implemented, authorization is expected to be managed within the application itself, depending on the user groups.

Users that don't exist yet may be added automatically by enabling the option `TACACSPLUS_AUTOCREATE_USERS`. Newly created users will be added with the standard django parameters `is_admin=False` and `is_staff=False`.

If you have customized User tables then this package may not work as expected.

## Installation

Install the package with pip:

```python
pip3 install django-auth-tacacs
```

This package requires `tacacs-plus` to be installed.

Depending on the usage, it also requires one of the following packages:

- django
- nautobot
- netbox

## Usage

To use this package, you'll need to add the `TACACSPlusAuthenticationBackend` library to the `AUTHENTICATION_BACKENDS` configuration parameter. The order is important, if you have multiple authentication backends then you must configure them in the correct order.

You also need to add the `TACACS_PLUS` configuration parameters:

```python
TACACSPLUS_HOST = 'localhost'
TACACSPLUS_PORT = 49
TACACSPLUS_SECRET = 'super-secret'
TACACSPLUS_SESSION_TIMEOUT = 5
TACACSPLUS_AUTH_PROTOCOL = 'ascii'
TACACSPLUS_AUTOCREATE_USERS = True
```

### Django example

This example will use the Tacacs+ authentication backend and fallback to the internal django DB user authentication:
Add the following to `settings.py`

```python
AUTHENTICATION_BACKENDS = [
    'django_auth_tacacs.django.TACACSPlusAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]
TACACSPLUS_HOST = 'localhost'
TACACSPLUS_PORT = 49
TACACSPLUS_SECRET = 'super-secret'
TACACSPLUS_SESSION_TIMEOUT = 5
TACACSPLUS_AUTH_PROTOCOL = 'ascii'
TACACSPLUS_AUTOCREATE_USERS = True 
```

### Nautobot example

This example will use the Tacacs+ authentication backend and fallback to the internal nautobot DB user authentication.  
Add the following to `nautobot_config.py`

```python
AUTHENTICATION_BACKENDS = [
     'django_auth_tacacs.nautobot.TACACSPlusAuthenticationBackend',
     'nautobot.core.authentication.ObjectPermissionBackend',
]
TACACSPLUS_HOST = 'localhost'
TACACSPLUS_PORT = 49
TACACSPLUS_SECRET = 'super-secret'
TACACSPLUS_SESSION_TIMEOUT = 5
TACACSPLUS_AUTH_PROTOCOL = 'ascii'
TACACSPLUS_AUTOCREATE_USERS = True 
```

### Netbox example

This example will use the Tacacs+ authentication backend and fallback to the internal netbox DB user authentication.  
Add the following to `configuration.py`

```python
REMOTE_AUTH_BACKEND = 'django_auth_tacacs.nautobot.TACACSPlusAuthenticationBackend'

TACACSPLUS_HOST = 'localhost'
TACACSPLUS_PORT = 49
TACACSPLUS_SECRET = 'super-secret'
TACACSPLUS_SESSION_TIMEOUT = 5
TACACSPLUS_AUTH_PROTOCOL = 'ascii'
TACACSPLUS_AUTOCREATE_USERS = True 
```
