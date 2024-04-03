from django.test import TestCase
from rest_framework.test import APIClient
from src.v1.test import (
    create_normal_user,
    create_employee_user,
    create_reply_request_body,
    create_support_ticket_request_body,
)


class ReplyTestCase(TestCase):
    """
    Test case for the Reply model.
    """
    def setUp(self):
        """
        Set up the test case:
        - Create a normal user
        - Set up the API client with the user's auth token
        - Set the endpoint for the support ticket API
        """
        self.test_user = create_normal_user()
        self.auth_token = self.test_user.auth_token
        self.end_point = "/api/v1/support_ticket"
        self.reply_end_point = "/api/v1/reply"

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token.key)
        self.client.default_format = "json"

    def test_normal_user_rely_support_ticket(self):
        """
        Test that a normal user can reply to a support ticket.
        """
        # Create a support ticket
        support_ticket_request_body = create_support_ticket_request_body()
        response = self.client.post(self.end_point, support_ticket_request_body)
        self.assertEqual(response.status_code, 201)

        # Reply to the support ticket
        reply_request_body = create_reply_request_body()
        support_ticket_id = response.data.get("id")
        response = self.client.post(f"{self.end_point}/{support_ticket_id}/reply", reply_request_body)
        self.assertEqual(response.status_code, 201)

        # Check the reply data
        self.assertEqual(response.data.get("content"), reply_request_body.get("content").lower())
        self.assertEqual(response.data.get("ticket"), support_ticket_id)
        self.assertEqual(response.data.get("replier"), self.test_user.id)

        # Check the ticket status after replying
        response = self.client.get(f"{self.end_point}/{support_ticket_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("status"), "REVIEWING")

    def test_normal_user_rely_support_ticket_with_invalid_ticket_id(self):
        """
        Test that replying to a non-existent ticket returns a 404 error.
        """
        reply_request_body = create_reply_request_body()
        response = self.client.post(f"{self.end_point}/9999/reply", reply_request_body)
        self.assertEqual(response.status_code, 404)

    def test_normal_user_rely_support_ticket_with_empty_content(self):
        """
        Test that replying with empty content returns a 400 error.
        """
        # Create a support ticket
        support_ticket_request_body = create_support_ticket_request_body()
        response = self.client.post(self.end_point, support_ticket_request_body)
        self.assertEqual(response.status_code, 201)

        # Reply to the support ticket with empty content
        reply_request_body = create_reply_request_body()
        reply_request_body["content"] = ""
        support_ticket_id = response.data.get("id")
        response = self.client.post(f"{self.end_point}/{support_ticket_id}/reply", reply_request_body)
        self.assertEqual(response.status_code, 400)

    def test_employee_user_rely_support_ticket(self):
        """
        Test that an employee user can reply to a support ticket.
        """
        # Create a support ticket
        support_ticket_request_body = create_support_ticket_request_body()
        response = self.client.post(self.end_point, support_ticket_request_body)
        self.assertEqual(response.status_code, 201)
        support_ticket_id = response.data.get("id")

        # Create an employee user and set up a client for the employee user
        employee_user = create_employee_user()
        employee_token = employee_user.auth_token
        employee_client = APIClient()
        employee_client.credentials(HTTP_AUTHORIZATION="Token " + employee_token.key)
        employee_client.default_format = "json"

        # Assign the ticket to the employee user
        assign_response = employee_client.put(
            f"{self.end_point}/{support_ticket_id}/assign?user_id={employee_user.id}",
        )
        self.assertEqual(assign_response.status_code, 200)

        # Reply to the ticket
        reply_request_body = create_reply_request_body()
        response = employee_client.post(f"{self.end_point}/{support_ticket_id}/reply", reply_request_body)
        self.assertEqual(response.status_code, 201)

        # Check the reply data
        self.assertEqual(response.data.get("content"), reply_request_body.get("content").lower())
        self.assertEqual(response.data.get("ticket"), support_ticket_id)
        self.assertEqual(response.data.get("replier"), employee_user.id)

        # Check the ticket status after replying
        response = employee_client.get(f"{self.end_point}/{support_ticket_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("status"), "WAIT_FOR_REPLY")
    
    def test_employee_user_rely_support_ticket_with_invalid_ticket_id(self):
        """
        Test that replying to a non-existent ticket returns a 404 error.
        """
        employee_user = create_employee_user()
        employee_token = employee_user.auth_token
        employee_client = APIClient()
        employee_client.credentials(HTTP_AUTHORIZATION="Token " + employee_token.key)
        employee_client.default_format = "json"

        reply_request_body = create_reply_request_body()
        response = employee_client.post(f"{self.end_point}/9999/reply", reply_request_body)
        self.assertEqual(response.status_code, 404)

    def test_edit_last_reply(self):
        """
        Test that a user can edit a reply.
        """
        # Create a support ticket
        support_ticket_request_body = create_support_ticket_request_body()
        response = self.client.post(self.end_point, support_ticket_request_body)
        self.assertEqual(response.status_code, 201)

        # Reply to the support ticket
        reply_request_body = create_reply_request_body()
        support_ticket_id = response.data.get("id")
        response = self.client.post(f"{self.end_point}/{support_ticket_id}/reply", reply_request_body)
        self.assertEqual(response.status_code, 201)
        reply_id = response.data.get("id")

        # Edit the reply
        new_content = "New content"
        response = self.client.put(f"{self.reply_end_point}/{reply_id}", {"content": new_content})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("content"), new_content.lower())

    def test_edit_not_last_reply(self):
        """
        Test that a user can't edit a reply that is not the last reply.
        """
        # Create a support ticket
        support_ticket_request_body = create_support_ticket_request_body()
        response = self.client.post(self.end_point, support_ticket_request_body)
        self.assertEqual(response.status_code, 201)

        # Reply to the support ticket
        reply_request_body = create_reply_request_body()
        support_ticket_id = response.data.get("id")
        response = self.client.post(f"{self.end_point}/{support_ticket_id}/reply", reply_request_body)
        self.assertEqual(response.status_code, 201)
        reply_id = response.data.get("id")

        # Reply to the support ticket again
        response = self.client.post(f"{self.end_point}/{support_ticket_id}/reply", reply_request_body)
        self.assertEqual(response.status_code, 201)

        # Edit the first reply
        new_content = "New content"
        response = self.client.put(f"{self.reply_end_point}/{reply_id}", {"content": new_content})
        self.assertEqual(response.status_code, 400)

    def test_edit_reply_with_not_own(self):
        """
        Test that a user can't edit a reply that not own.
        """
        # Create a support ticket
        support_ticket_request_body = create_support_ticket_request_body()
        response = self.client.post(self.end_point, support_ticket_request_body)
        self.assertEqual(response.status_code, 201)

        # Reply to the support ticket
        reply_request_body = create_reply_request_body()
        support_ticket_id = response.data.get("id")
        response = self.client.post(f"{self.end_point}/{support_ticket_id}/reply", reply_request_body)
        self.assertEqual(response.status_code, 201)
        reply_id = response.data.get("id")

        # Create an employee user and set up a client for the employee user
        employee_user = create_employee_user()
        employee_token = employee_user.auth_token
        employee_client = APIClient()
        employee_client.credentials(HTTP_AUTHORIZATION="Token " + employee_token.key)
        employee_client.default_format = "json"

        # Edit the reply
        new_content = "New content"
        response = employee_client.put(f"{self.reply_end_point}/{reply_id}", {"content": new_content})
        self.assertEqual(response.status_code, 404)
    
    def test_delete_reply(self):
        """
        Test that a user can delete a reply.
        """
        # Create a support ticket
        support_ticket_request_body = create_support_ticket_request_body()
        response = self.client.post(self.end_point, support_ticket_request_body)
        self.assertEqual(response.status_code, 201)

        # Reply to the support ticket
        reply_request_body = create_reply_request_body()
        support_ticket_id = response.data.get("id")
        response = self.client.post(f"{self.end_point}/{support_ticket_id}/reply", reply_request_body)
        self.assertEqual(response.status_code, 201)
        reply_id = response.data.get("id")

        # Delete the reply
        response = self.client.delete(f"{self.reply_end_point}/{reply_id}")
        self.assertEqual(response.status_code, 204)

    def test_delete_reply_with_not_own(self):
        """
        Test that a user can't delete a reply that not own.
        """
        # Create a support ticket
        support_ticket_request_body = create_support_ticket_request_body()
        response = self.client.post(self.end_point, support_ticket_request_body)
        self.assertEqual(response.status_code, 201)

        # Reply to the support ticket
        reply_request_body = create_reply_request_body()
        support_ticket_id = response.data.get("id")
        response = self.client.post(f"{self.end_point}/{support_ticket_id}/reply", reply_request_body)
        self.assertEqual(response.status_code, 201)
        reply_id = response.data.get("id")

        # Create an employee user and set up a client for the employee user
        employee_user = create_employee_user()
        employee_token = employee_user.auth_token
        employee_client = APIClient()
        employee_client.credentials(HTTP_AUTHORIZATION="Token " + employee_token.key)
        employee_client.default_format = "json"

        # Delete the reply
        response = employee_client.delete(f"{self.reply_end_point}/{reply_id}")
        self.assertEqual(response.status_code, 404)
