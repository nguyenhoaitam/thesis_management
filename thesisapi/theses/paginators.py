from rest_framework import pagination


class BasePaginator(pagination.PageNumberPagination):
    page_size = 5


class ThesisPaginator(pagination.PageNumberPagination):
    page_size = 5


class PostCommentPaginator(pagination.PageNumberPagination):
    page_size = 6
