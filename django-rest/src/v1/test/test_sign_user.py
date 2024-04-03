from src.v1.test import create_sign_up_request_body

from django.test import TestCase

from rest_framework.test import APIClient


class SignUserTestCase(TestCase):
    """
    Test case for user sign up and sign in.
    """
    def setUp(self):
        """
        Set up the test case:
        - Set the username and password
        - Set the endpoint for the sign user API
        - Set up the API client
        """
        self.username = "tester123"
        self.password = "test_password456"
        self.end_point = "/api/v1/sign_user"

        self.client = APIClient()
        self.client.default_format = "json"

    def test_sign_up(self):
        """
        Test user sign up.
        """
        sign_up_request_body = create_sign_up_request_body()
        sign_up_request_body["username"] = self.username
        sign_up_request_body["password"] = self.password
        sign_up_request_body["is_employee"] = False

        response = self.client.post(f"{self.end_point}/sign-up", sign_up_request_body)
        self.assertEqual(response.status_code, 201)

    def test_sign_in(self):
        """
        Test user sign in.
        """
        # Sign up a user
        sign_up_request_body = create_sign_up_request_body()
        sign_up_request_body["username"] = self.username
        sign_up_request_body["password"] = self.password
        sign_up_request_body["is_employee"] = False

        response = self.client.post(f"{self.end_point}/sign-up", sign_up_request_body)
        self.assertEqual(response.status_code, 201)

        # Sign in the user
        sign_in_request_body = {
            "username": self.username,
            "password": self.password,
        }

        response = self.client.post(f"{self.end_point}/sign-in", sign_in_request_body)
        self.assertEqual(response.status_code, 200)
        user_id = response.data["user_id"]
        token = response.data["token"]

        # Check the user's details
        self.client.credentials(HTTP_AUTHORIZATION=token)

        response = self.client.get(f"/api/v1/user/{user_id}")
        self.assertEqual(response.status_code, 200)