from src.v1.models import Reply

from rest_framework import serializers


class ReplySerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving the details of a reply.
    """
    class Meta:
        model = Reply
        fields = [
            "id",
            "ticket",
            "content",
            "replier",
            "update_time"
        ]

    def to_representation(self, instance):
        """
        Override the default representation to return the IDs of the ticket and replier.
        """
        return {
            "id": instance.id,
            "ticket": instance.ticket.id,
            "content": instance.content,
            "replier": instance.replier.id,
            "update_time": instance.update_time
        }


class ListReplySerializer(serializers.ModelSerializer):
    """
    Serializer for listing all replies.
    """
    class Meta:
        model = Reply
        fields = [
            "id",
            "content",
            "replier",
            "is_active",
            "update_time"
        ]

    def __init__(self, *args, **kwargs):
        """
        Initialize the serializer and get the support ticket from the context.
        """
        super(ListReplySerializer, self).__init__(*args, **kwargs)
        self.support_ticket = self.context.get("support_ticket")

    def to_representation(self, instance):
        """
        Override the default representation to only return replies for the support ticket.
        """
        data = super().to_representation(instance)
        if self.support_ticket and instance.ticket == self.support_ticket:
            return data
        return []


class CreateReplySerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new reply.
    """
    class Meta:
        model = Reply
        fields = [
            "content",
        ]

    def to_representation(self, instance):
        """
        Use the ReplySerializer to represent the created reply.
        """
        return ReplySerializer(instance).data

    def validate(self, data):
        """
        Validate the data:
        - Raise an error if no content is provided
        - Lowercase content
        """
        if not data.get("content"):
            raise serializers.ValidationError(
                {
                    "detail": "No data provided!"
                }
            )

        data["content"] = data["content"].lower()
        return data

    def create(self, validated_data):
        """
        Create a new reply.
        - Assign the ticket and replier from the context
        """
        request = self.context["request"]
        ticket = self.context["support_ticket"]
        replier = request.user

        validated_data["ticket"] = ticket
        validated_data["replier"] = replier

        return Reply.objects.create(**validated_data)


class EditReplySerializer(serializers.ModelSerializer):
    """
    Serializer for editing a reply.
    """
    class Meta:
        model = Reply
        fields = [
            "content",
        ]

    def to_representation(self, instance):
        """
        Use the ReplySerializer to represent the updated reply.
        """
        return ReplySerializer(instance).data

    def validate(self, data):
        """
        Validate the data:
        - Raise an error if no content is provided
        - Lowercase content
        """
        if not data.get("content"):
            raise serializers.ValidationError(
                {
                    "detail": "No data provided!"
                }
            )
        
        data["content"] = data["content"].lower()
        return data

    def update(self, instance, validated_data):
        """
        Update a reply.
        - Only allow to edit the latest reply for each ticket
        """
        latest_reply = Reply.objects.filter(
            ticket=instance.ticket,
            is_active=True
        ).order_by("-create_time").first()

        if latest_reply.id != instance.id:
            raise serializers.ValidationError(
                {
                    "detail": "This reply does not allow to edit!"
                }
            )

        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance
