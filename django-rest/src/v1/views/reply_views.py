from src.v1.models import Reply
from src.v1.filters.ids_filter_backend import IdsFilterBackend
from src.v1.filters.name_filter_backend import NameFilterBackend
from src.v1.filters.support_ticket_filter_backend import SupportTicketFilterBackend
from src.v1.paginations.custom_page_number_pagination import CustomPageNumberPagination
from src.v1.serializers.reply_serializers import (
    CreateReplySerializer,
    ListReplySerializer,
    EditReplySerializer
)

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, authentication, status, filters


class ReplyModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated,]
    pagination_class = CustomPageNumberPagination
    filter_backends = [
        IdsFilterBackend,
        NameFilterBackend,
        SupportTicketFilterBackend,
        filters.OrderingFilter,
    ]

    def get_queryset(self):
        user = self.request.user
        
        # only repler can edit/delete own reply
        return Reply.objects.filter(
            replier=user,
            is_active=True)

    def get_serializer_class(self):
        if self.action == "update":
            return EditReplySerializer

        raise NotImplementedError()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )