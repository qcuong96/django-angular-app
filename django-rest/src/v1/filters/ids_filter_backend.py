from rest_framework import filters

class IdsFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        ids = query_params.get("ids")
        if ids:
            ids = ids.split(",")
            queryset = queryset.filter(id__in=ids)

        return queryset
