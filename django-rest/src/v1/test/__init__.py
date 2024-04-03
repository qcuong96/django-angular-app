from faker import Faker
from faker import Factory

from src.v1.test.factories.user_factory import UserFactory


faker = Factory.create()


def create_normal_user():
    return UserFactory()


def create_employee_user():
    return UserFactory(is_employee=True)


def create_support_ticket_request_body():
    return {
        "name": faker.sentence(),
        "description": faker.text(),
    }


def create_reply_request_body():
    return {
        "content": faker.text(),
    }


def create_sign_up_request_body():
    return {
        "email": faker.email(),
        "password": faker.password(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "phone": Faker().numerify(text="##########"),
    }