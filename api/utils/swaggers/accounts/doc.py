import os
from utils.swaggers import base as swager_baase
from drf_yasg import openapi


list_users = [
    swager_baase.make_api_param(
        "system-key",
        openapi.IN_HEADER,
        "시스템 키",
        openapi.TYPE_STRING,
        os.environ.get("SYSTEM_KEY"),
    ),
]

signup = [
    swager_baase.make_api_param(
        "system-key",
        openapi.IN_HEADER,
        "시스템 키",
        openapi.TYPE_STRING,
        os.environ.get("SYSTEM_KEY"),
    ),
]
