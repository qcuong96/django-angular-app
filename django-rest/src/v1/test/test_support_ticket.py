from src.v1.test import (
    create_employee_user,
    create_normal_user,
    create_support_ticket_request_body,
)

from django.test import TestCase

from rest_framework.test import APIClient


class SupportTicketTestCase(TestCase):
    def setUp(self):
        normal_user = create_normal_user()

        self.auth_token = normal_user.auth_token
        self.end_point = "/api/v1/support_ticket"

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token.key)
        client.default_format = "json"

        self.client = client

    def _create_support_ticket(self):
        request_body = create_support_ticket_request_body()
        return self.client.post(self.end_point, request_body), request_body

    def test_create_support_ticket(self):
        create_response, request_body = self._create_support_ticket()
        self.assertEqual(create_response.status_code, 201)

        create_response_data = create_response.data
        self.assertEqual(request_body["name"].lower(),
                         create_response_data["name"])
        self.assertEqual(request_body["description"].lower(),
                         create_response_data["description"])

    def test_create_support_ticket_unauthorized(self):
        unauthorized_client = APIClient()
        unauthorized_client.default_format = "json"
        create_response = unauthorized_client.post(
            self.end_point, create_support_ticket_request_body())
        self.assertEqual(create_response.status_code, 401)

    def test_edit_support_ticket(self):
        create_response, request_body = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        edit_request_body = create_support_ticket_request_body()
        edit_response = self.client.put(
            f"{self.end_point}/{support_ticket_id}", edit_request_body
        )
        self.assertEqual(edit_response.status_code, 200)

        edit_response_data = edit_response.data
        self.assertEqual(edit_request_body["name"].lower(),
                         edit_response_data["name"])
        self.assertEqual(edit_request_body["description"].lower(),
                         edit_response_data["description"])
    
    def test_edit_support_ticket_name_only(self):
        create_response, request_body = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        edit_request_body = create_support_ticket_request_body()
        edit_request_body.pop("description")
        edit_response = self.client.put(
            f"{self.end_point}/{support_ticket_id}", edit_request_body
        )
        self.assertEqual(edit_response.status_code, 200)

        edit_response_data = edit_response.data
        self.assertEqual(edit_request_body["name"].lower(),
                         edit_response_data["name"])
        self.assertEqual(request_body["description"].lower(),
                         edit_response_data["description"])
        
    def test_edit_support_ticket_description_only(self):
        create_response, request_body = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        edit_request_body = create_support_ticket_request_body()
        edit_request_body.pop("name")
        edit_response = self.client.put(
            f"{self.end_point}/{support_ticket_id}", edit_request_body
        )
        self.assertEqual(edit_response.status_code, 200)

        edit_response_data = edit_response.data
        self.assertEqual(request_body["name"].lower(),
                         edit_response_data["name"])
        self.assertEqual(edit_request_body["description"].lower(),
                         edit_response_data["description"])
        
    def test_edit_support_ticket_priority_only(self):
        create_response, request_body = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        edit_response = self.client.put(
            f"{self.end_point}/{support_ticket_id}", {"priority": "HIGH"}
        )
        self.assertEqual(edit_response.status_code, 200)

        edit_response_data = edit_response.data
        self.assertEqual(request_body["name"].lower(),
                         edit_response_data["name"])
        self.assertEqual(request_body["description"].lower(),
                         edit_response_data["description"])
        
    def test_edit_support_ticket_category_only(self):
        create_response, request_body = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        edit_response = self.client.put(
            f"{self.end_point}/{support_ticket_id}", {"category": "ISSUE"}
        )
        self.assertEqual(edit_response.status_code, 200)

        edit_response_data = edit_response.data
        self.assertEqual(request_body["name"].lower(),
                         edit_response_data["name"])
        self.assertEqual(request_body["description"].lower(),
                         edit_response_data["description"])

    def test_edit_support_ticket_not_found(self):
        edit_request_body = create_support_ticket_request_body()
        edit_response = self.client.put(
            f"{self.end_point}/999999", edit_request_body
        )
        self.assertEqual(edit_response.status_code, 404)

    def test_edit_support_ticket_empty_request_body(self):
        create_response, _ = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        edit_response = self.client.put(
            f"{self.end_point}/{support_ticket_id}", {}
        )
        self.assertEqual(edit_response.status_code, 400)

    def test_edit_support_ticket_empty_values(self):
        create_response, _ = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        edit_request_body = create_support_ticket_request_body()
        edit_request_body["name"] = ""
        edit_request_body["description"] = ""
        edit_response = self.client.put(
            f"{self.end_point}/{support_ticket_id}", edit_request_body
        )
        self.assertEqual(edit_response.status_code, 400)

    def test_edit_support_ticket_unauthorized(self):
        create_response, _ = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        edit_request_body = create_support_ticket_request_body()
        unauthorized_client = APIClient()
        unauthorized_client.default_format = "json"
        edit_response = unauthorized_client.put(
            f"{self.end_point}/{support_ticket_id}", edit_request_body
        )
        self.assertEqual(edit_response.status_code, 401)

    def test_close_support_ticket(self):
        create_response, _ = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        close_response = self.client.put(
            f"{self.end_point}/{support_ticket_id}/close"
        )
        self.assertEqual(close_response.status_code, 200)

        close_response_data = close_response.data
        self.assertEqual("DONE", close_response_data["status"])

    def test_close_support_ticket_not_found(self):
        close_response = self.client.put(
            f"{self.end_point}/999999/close"
        )
        self.assertEqual(close_response.status_code, 404)
    
    def test_close_support_ticket_unauthorized(self):
        create_response, _ = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        unauthorized_client = APIClient()
        unauthorized_client.default_format = "json"
        close_response = unauthorized_client.put(
            f"{self.end_point}/{support_ticket_id}/close"
        )
        self.assertEqual(close_response.status_code, 401)

    def test_assign_support_ticket(self):
        create_response, _ = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        employee_user = create_employee_user()
        employee_token = employee_user.auth_token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + employee_token.key)
        client.default_format = "json"

        assign_response = client.put(
            f"{self.end_point}/{support_ticket_id}/assign?user_id={employee_user.id}",
        )
        self.assertEqual(assign_response.status_code, 200)

        assign_response_data = assign_response.data
        self.assertEqual(employee_user.username, assign_response_data["supporter"])
    
    def test_employee_user_close_support_ticket_after_assigned(self):
        create_response, _ = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        employee_user = create_employee_user()
        employee_token = employee_user.auth_token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + employee_token.key)
        client.default_format = "json"

        assign_response = client.put(
            f"{self.end_point}/{support_ticket_id}/assign?user_id={employee_user.id}",
        )
        self.assertEqual(assign_response.status_code, 200)

        close_response = client.put(
            f"{self.end_point}/{support_ticket_id}/close"
        )
        self.assertEqual(close_response.status_code, 200)

        close_response_data = close_response.data
        self.assertEqual("DONE", close_response_data["status"])

    def test_employee_user_close_support_ticket_before_assigned(self):
        create_response, _ = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        employee_user = create_employee_user()
        employee_token = employee_user.auth_token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + employee_token.key)
        client.default_format = "json"

        close_response = client.put(
            f"{self.end_point}/{support_ticket_id}/close"
        )
        self.assertEqual(close_response.status_code, 403)

    def test_assgin_support_ticket_not_found(self):
        employee_user = create_employee_user()
        employee_token = employee_user.auth_token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + employee_token.key)
        client.default_format = "json"

        assign_response = client.put(
            f"{self.end_point}/99999/assign?user_id={employee_user.id}",
        )
        self.assertEqual(assign_response.status_code, 404)

    def test_assign_support_ticket_to_normal_user(self):
        create_response, _ = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        normal_user = create_normal_user()
        normal_token = normal_user.auth_token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + normal_token.key)
        client.default_format = "json"

        assign_response = client.put(
            f"{self.end_point}/{support_ticket_id}/assign?user_id={normal_user.id}",
        )
        self.assertEqual(assign_response.status_code, 400)

    def test_assign_support_ticket_unauthorized(self):
        create_response, _ = self._create_support_ticket()
        support_ticket_id = create_response.data["id"]

        employee_user = create_employee_user()
        client = APIClient()
        client.default_format = "json"

        assign_response = client.put(
            f"{self.end_point}/{support_ticket_id}/assign?user_id={employee_user.id}",
        )
        self.assertEqual(assign_response.status_code, 401)
