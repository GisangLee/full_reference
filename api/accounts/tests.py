import pytest, os
from django.conf import settings
from django.test import TestCase, Client
from model_mommy.recipe import Recipe
from rest_framework import status
from api.accounts import models as account_models


@pytest.mark.django_db
class TestAccountViewSet(TestCase):
    def setUp(self):
        self.client = Client()
        self.account_recipe = Recipe(account_models.User)

    @classmethod
    def setUpTestData(cls):
        data = {
            "id": "test",
            "keywords": "keyw",
            "subscriptions": "main",
        }
        response = TestAccountViewSet.client.post(
            "http://127.0.0.1:8000/api-v1/accounts/",
            data=data,
            content_type="application/json",
        )

    def test_accounts_create_action(self):

        user = self.account_recipe.make()

        post_data = {
            "name": "장고",
            "email": "django@gmail.com",
            "password": "qwe123",
            "gender": "M",
            "age": 30,
        }

        response = self.client.post(
            "http://127.0.0.1:8000/api-v1/accounts/", data=post_data, follow=True
        )

    def test_accounts_list_action(self):

        header = {"system-key": os.environ.get("SYSTEM_KEY")}
        response = self.client.get("http://127.0.0.1:8000/api-v1/accounts/", **header)

        assert status.is_success(response.status_code)

    def test_accouts_retrieve_action(self):
        header = {"Authorization": "jwt "}
        response = self.client.get("http://127.0.0.1:8000/api-v1/accounts/1/", **header)

        assert status.HTTP_400_BAD_REQUEST == response.status_code
