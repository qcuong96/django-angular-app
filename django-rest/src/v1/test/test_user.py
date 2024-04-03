from src.v1.test import (
    create_employee_user,
    create_normal_user,
)

from django.test import TestCase

from rest_framework.test import APIClient


class UserTestCase(TestCase):
    test_user = None

    def setUp(self):
        employee_user = create_employee_user()
        self.test_user = employee_user

        self.auth_token = employee_user.auth_token
        self.end_point = "/api/v1/user"

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token.key)
        client.default_format = "json"

        self.client = client

    def test_get_user_info(self):
        response = self.client.get(self.end_point + f"/{self.test_user.id}")
        self.assertEqual(response.status_code, 200)

    def test_get_user_list(self):
        response = self.client.get(self.end_point)
        self.assertEqual(response.status_code, 200)

    def test_normal_user_get_user_list(self):
        normal_user = create_normal_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + normal_user.auth_token.key)
        client.default_format = "json"

        response = client.get(self.end_point)
        self.assertEqual(response.status_code, 403)
