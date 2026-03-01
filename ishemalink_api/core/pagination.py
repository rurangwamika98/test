from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MobilePageNumberPagination(PageNumberPagination):
    page_size_query_param = "size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "meta": {
                    "total_count": self.page.paginator.count,
                    "current_page": self.page.number,
                    "next_link": self.get_next_link(),
                },
                "data": data,
            }
        )
