from rest_framework import filters


class SupportTicketFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        status = query_params.get("status")
        priority = query_params.get("priority")
        category = query_params.get("category")

        try:
            assigned_to = query_params["assigned_to"]
            assigned_to = True
        except:
            assigned_to = False

        if status:
            queryset = queryset.filter(status=status.upper())
        if priority:
            queryset = queryset.filter(priority=priority.upper())
        if category:
            queryset = queryset.filter(category=category.upper())
        if assigned_to:
            queryset = queryset.filter(supporter=request.user)

        return queryset