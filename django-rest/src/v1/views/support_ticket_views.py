from src.v1.models import Reply, SupportTicket, User
from src.v1.filters.ids_filter_backend import IdsFilterBackend
from src.v1.filters.name_filter_backend import NameFilterBackend
from src.v1.filters.support_ticket_filter_backend import SupportTicketFilterBackend
from src.v1.paginations.custom_page_number_pagination import CustomPageNumberPagination
from src.v1.serializers.reply_serializers import CreateReplySerializer, ListReplySerializer
from src.v1.serializers.support_ticket_serializers import (
    CreateSupportTicketSerializer,
    ListSupportTicketSerializer,
    DetailsSupportTicketSerializer,
    EditSupportTicketSerializer
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, authentication, status, filters


class SupportTicketModelViewSet(viewsets.ModelViewSet):
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
        # user can get only his/her support tickets
        # staff can get all support tickets
        user = self.request.user
        if user.is_employee:
            return SupportTicket.objects.filter(
                is_active=True).order_by("-update_time", "-id")

        return SupportTicket.objects.filter(
            reporter=user, is_active=True).order_by("-update_time", "-id")

    def get_serializer_class(self):
        if self.action == "create":
            return CreateSupportTicketSerializer

        if self.action == "update":
            return EditSupportTicketSerializer

        if self.action == "retrieve":
            return DetailsSupportTicketSerializer

        return ListSupportTicketSerializer

    def perform_destroy(self, instance):
        instance.status = SupportTicket.STATUS_DELETE
        instance.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=True, methods=["PUT"], url_path="assign", name="Assign Support Ticket",
    )
    def assign_support_ticket(self, request, pk=None):
        user = request.user

        if not user.is_employee:
            return Response(
                {
                    "detail": "You must be an employee to assign support tickets."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        params = request.query_params
        user_id = params.get("user_id")

        if not user_id:
            return Response(
                {
                    "detail": "User ID is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        _user = User.objects.filter(
            id=user_id, is_active=True, is_employee=True).first()

        if not _user:
            return Response(
                {
                    "detail": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not user.is_staff and _user.id != user.id:
            return Response(
                {
                    "detail": "You can only assign support tickets to yourself."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        support_ticket = self.get_object()
        support_ticket.supporter = _user
        support_ticket.save()

        return Response(
            support_ticket.response(),
            status=status.HTTP_200_OK
        )

    @action(
        detail=True, methods=["POST"], url_path="reply", name="Reply to Support Ticket",
    )
    def reply_support_ticket(self, request, pk=None):
        user = request.user
        support_ticket = self.get_object()

        if not (
            user == support_ticket.reporter
            or user == support_ticket.supporter
        ):
            raise PermissionDenied(
                {
                    "detail": "You do not have permission to reply this ticket."
                }
            )
        
        serializer = CreateReplySerializer(
            data=request.data, context={
                "request": request, "support_ticket": support_ticket}
        )

        if serializer.is_valid():
            serializer.save()

            # if user is reporter, update ticket status to REVIEWING
            # if user is supporter, update ticket status to WAIT_FOR_REPLY
            if user == support_ticket.reporter:
                support_ticket.status = SupportTicket.STATUS_REVIEWING
            else:
                support_ticket.status = SupportTicket.STATUS_WAIT_FOR_REPLY

            support_ticket.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @reply_support_ticket.mapping.get
    def view_replies(self, request, pk=None):
        params = request.query_params
        support_ticket = self.get_object()

        try:
            params["view_deleted"]
            replies = Reply.objects.filter(ticket=support_ticket).order_by("create_time")
        except:
            replies = Reply.objects.filter(ticket=support_ticket, is_active=True).order_by("create_time")
        
        serializer = ListReplySerializer(replies, many=True, context={"request": request, "support_ticket": support_ticket})

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=True, methods=["PUT"], url_path="close", name="Close Support Ticket",
    )
    def close_support_ticket(self, request, pk=None):
        user = request.user
        support_ticket = self.get_object()

        if not (
            user == support_ticket.reporter
            or user == support_ticket.supporter
        ):
            raise PermissionDenied(
                {
                    "detail": "You do not have permission to close this ticket."
                }
            )

        support_ticket.status = SupportTicket.STATUS_DONE
        support_ticket.save()

        return Response(
            support_ticket.response(),
            status=status.HTTP_200_OK
        )
