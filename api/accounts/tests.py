import pytest, os
from django.conf import settings
from django.test import TestCase, Client
from rest_framework import status


@pytest.mark.django_db
class TestDevices(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     data = {
    #         "id": "test",
    #         "keywords": "keyw",
    #         "subscriptions": "main",
    #     }
    #     response = Client.post(
    #         "/accounts/device", data=data, content_type="application/json"
    #     )

    def test_accounts_device_get(self):
        data = {
            "id": "test",
        }
        header = {"system-key": os.environ.get("SYSTEM_KEY")}
        response = Client().get("http://127.0.0.1:8000/api-v1/accounts/", **header)

        assert status.is_success(response.status_code)
