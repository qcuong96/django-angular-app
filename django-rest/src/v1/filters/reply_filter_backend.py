from rest_framework import filters
from src.v1.models import SupportTicket


class ReplyFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        ticket_id = query_params.get("ticket_id")

        if ticket_id:
            ticket = SupportTicket.objects.filter(id=ticket_id).first()
        
            queryset = queryset.filter(ticket=ticket)

        return queryset
