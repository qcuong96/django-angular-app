from src.v1.models import SupportTicket

from datetime import timedelta

from django.utils import timezone

from rest_framework import serializers


class ListSupportTicketSerializer(serializers.ModelSerializer):
    """
    Serializer for listing all support tickets.
    """
    class Meta:
        model = SupportTicket
        fields = [
            "id",
            "name",
            "description",
            "priority",
            "category",
            "status",
            "create_time",
            "update_time",
        ]


class DetailsSupportTicketSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving the details of a support ticket.
    """
    class Meta:
        model = SupportTicket
        fields = [
            "id",
            "name",
            "description",
            "priority",
            "category",
            "status",
            "create_time",
            "update_time",
            "reporter",
            "supporter",
        ]

    def to_representation(self, instance):
        """
        Represent the ticket details.
        """
        data = super().to_representation(instance)
        data["reporter"] = instance.reporter.username
        data["supporter"] = instance.supporter.username if instance.supporter else None
        return data

class CreateSupportTicketSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new support ticket.
    """
    class Meta:
        model = SupportTicket
        fields = [
            "name",
            "description",
            "priority",
            "category",
            "reporter",
        ]

    def to_representation(self, instance):
        """
        Use the DetailsSupportTicketSerializer to represent the created ticket.
        """
        return DetailsSupportTicketSerializer(instance).data

    def validate(self, data):
        """
        Validate the data:
        - Lowercase name and description
        - Uppercase priority and category
        """
        data = {k: v.lower() if k in ["name", "description"] else v.upper() for k, v in data.items()}
        return data

    def create(self, validated_data):
        """
        Create a new support ticket.
        """
        user = self.context["request"].user
        
        if user.is_employee:
            raise serializers.ValidationError({"detail": "Only customers can create a support ticket!"})
        
        validated_data["reporter"] = user
        return SupportTicket.objects.create(**validated_data)


class EditSupportTicketSerializer(serializers.ModelSerializer):
    """
    Serializer for editing a support ticket.
    """
    class Meta:
        model = SupportTicket
        fields = [
            "name",
            "description",
            "priority",
            "category"
        ]

    def __init__(self, *args, **kwargs):
        """
        Make the name field optional for updates.
        """
        super(EditSupportTicketSerializer, self).__init__(*args, **kwargs)
        if self.instance is not None:  # if serializer is used for update
            self.fields['name'].required = False

    def to_representation(self, instance):
        """
        Use the DetailsSupportTicketSerializer to represent the updated ticket.
        """
        return DetailsSupportTicketSerializer(instance).data

    def validate(self, data):
        """
        Validate the data:
        - Raise an error if no data is provided
        - Lowercase name and description
        - Uppercase priority and category
        """
        if not data:
            raise serializers.ValidationError({"detail": "No data to update!"})

        data = {k: v.lower() if k in ["name", "description"] else v.upper() for k, v in data.items()}
        return data

    def update(self, instance, validated_data):
        """
        Update a support ticket.
        - Only allow to edit open tickets within an hour of creation
        """
        if instance.status != SupportTicket.STATUS_NEW \
                or instance.create_time + timedelta(hours=1) < timezone.now():
            raise serializers.ValidationError({"detail": "Only allow to edit open ticket in an hour!"})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
