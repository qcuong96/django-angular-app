# Create your models here.
import email
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.contrib.postgres.fields import ArrayField

DB_TABLE_PREFIX = "customer_service_"


class CustomerServiceMetaModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(null=False, default=True)

    class Meta:
        abstract = True

    # Get list of field name of model
    #   - params:
    #       + include_foreign_key: bool | if True, include foreign key field name, default is False
    @classmethod
    def get_field_names(cls, include_foreign_key=False):
        ret = []
        for field in cls._meta.fields:
            if not isinstance(field, models.ForeignKey):
                ret.append(field.name)
                continue

            if include_foreign_key:
                ret.append(field.name)

        return ret


class CustomerServiceMetaModelWithName(CustomerServiceMetaModel):
    name = models.TextField(max_length=200, null=False)

    class Meta:
        abstract = True


class Application(CustomerServiceMetaModel):
    """Data model contains application registered with Customer Service project:
    - Web application
    """

    api_key = models.CharField(max_length=200, null=False)
    secret_key = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = DB_TABLE_PREFIX + "application"


class User(AbstractUser):
    avatar_url = models.TextField(max_length=250, null=True)
    phone = models.CharField(max_length=15, null=True)
    is_employee = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.first_name or self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        return self.username

    class Meta:
        db_table = DB_TABLE_PREFIX + "user"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class PermissionMetadata(models.Model):
    permission = models.OneToOneField(Permission, on_delete=models.CASCADE)
    is_template = models.BooleanField(default=False)
    module = models.CharField(max_length=255, null=False, default="")

    class Meta:
        db_table = DB_TABLE_PREFIX + "permission_metadata"


class GroupMetadata(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    is_editable = models.BooleanField(default=True)

    class Meta:
        db_table = DB_TABLE_PREFIX + "group_metadata"


class SupportTicket(CustomerServiceMetaModelWithName):
    """Data model contains support ticket created by user
    """
    STATUS_NEW = "NEW"
    STATUS_REVIEWING = "REVIEWING"
    STATUS_WAIT_FOR_REPLY = "WAIT_FOR_REPLY"
    STATUS_DONE = "DONE"
    STATUS_DELETE = "DELETE"

    STATUSES = (
        (STATUS_NEW, "A new created ticket"),
        (STATUS_REVIEWING, "A ticket is reviewing by support team"),
        (STATUS_WAIT_FOR_REPLY, "A ticket is waiting for reply from user"),
        (STATUS_DONE, "A ticket is resolved"),
        (STATUS_DELETE, "A ticket is deleted"),
    )

    PRIORITY_LOW = "LOW"
    PRIORITY_NORMAL = "NORMAL"
    PRIORITY_HIGH = "HIGH"

    PRIORITIES = (
        (PRIORITY_LOW, "Ticket need to be reviewed in 3 days"),
        (PRIORITY_NORMAL, "Ticket need to be reviewed in 1 day"),
        (PRIORITY_HIGH, "Ticket need to be reviewed in 12 hours"),
    )

    CATEGORY_HIRE = "HIRE"
    CATEGORY_RETURN = "RETURN"
    CATEGORY_ISSUE = "ISSUE"
    CATEGORY_LOST = "LOST"
    CATEGORY_OTHER = "OTHER"

    CATEGORIES = (
        (CATEGORY_HIRE, "Ticket for hiring service"),
        (CATEGORY_RETURN, "Ticket for returning service"),
        (CATEGORY_ISSUE, "Ticket for issue service"),
        (CATEGORY_LOST, "Ticket for lost service"),
        (CATEGORY_OTHER, "Ticket for other service"),
    )
    

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50, null=False, default=STATUS_NEW, choices=STATUSES)
    priority = models.CharField(max_length=50, null=False, default=PRIORITY_NORMAL, choices=PRIORITIES)
    category = models.CharField(max_length=50, null=False, default=CATEGORY_OTHER, choices=CATEGORIES)
    supporter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="supporter")
    description = models.TextField(max_length=5000, null=True)
    
    class Meta:
        db_table = DB_TABLE_PREFIX + "support_ticket"

    def response(self):
        return {
            "id": self.id,
            "name": self.name,
            "reporter": self.reporter.username,
            "status": self.status,
            "priority": self.priority,
            "category": self.category,
            "description": self.description,
            "supporter": self.supporter.username if self.supporter else None,
            "create_time": self.create_time,
            "update_time": self.update_time,
        }


class Reply(CustomerServiceMetaModel):
    """Data model contains reply to support ticket
    """

    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE)
    replier = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=5000, null=False)
    attachments = ArrayField(models.TextField(max_length=250), default=list)

    class Meta:
        db_table = DB_TABLE_PREFIX + "reply"

    def response(self):
        return {
            "id": self.id,
            "ticket_id": self.ticket.id,
            "replier": self.replier.username,
            "content": self.content,
            "update_time": self.update_time,
        }