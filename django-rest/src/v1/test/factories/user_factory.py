import factory
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating User model instances for testing.
    """
    class Meta:
        model = "v1.User"
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"testuser{n}")  # Create a unique username
    password = factory.Faker(
        "password",
        length=10,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True,
    )  # Generate a random password
    email = factory.Faker("email")  # Generate a random email
    first_name = factory.Faker("first_name")  # Generate a random first name
    last_name = factory.Faker("last_name")  # Generate a random last name
    phone = factory.LazyAttribute(lambda _: fake.numerify(text="##########"))  # Generate a random 10-digit phone number
    is_active = True  # Set the user as active
    is_staff = False  # Set the user as not staff
    is_employee = False  # Set the user as not an employee