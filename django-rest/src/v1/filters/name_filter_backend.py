from rest_framework import filters

class NameFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        name_kw = query_params.get("name")
        if name_kw:
            name_kw = " ".join(name_kw.lower().split())
            queryset = queryset.filter(name__icontains=name_kw)

        return queryset
