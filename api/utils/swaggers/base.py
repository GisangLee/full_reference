from drf_yasg import openapi


def make_api_param(name, type, desc, format, default=""):
    param = openapi.Parameter(
        name, type, description=desc, type=format, default=default
    )

    return param
