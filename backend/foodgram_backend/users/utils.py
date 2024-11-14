import re

from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation

from .constants import USERNAME_PATTERN
from django.core.exceptions import ValidationError

