from django.core.paginator import Paginator


class PaginatedListViewMixin:
    paginate_by = 1
