from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Пагинатор с переопределенным запрошенным количеством страниц."""

    page_size_query_param = 'limit'
