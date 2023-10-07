from typing import Dict

from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ResponseManager:
    """Utility class that abstracts how we create a DRF response"""

    @staticmethod
    def handle_response(
        data: Dict = {}, errors: Dict = {}, status: int = 200, message: str = ""
    ) -> Response:
        if errors:
            return Response({"errors": errors, "message": message}, status=status)
        return Response({"data": data, "message": message}, status=status)

    @staticmethod
    def handle_paginated_response(
        paginator_instance: PageNumberPagination = PageNumberPagination(),
        data: Dict = {},
    ) -> Response:
        return paginator_instance.get_paginated_response(data)


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["https", "http"]
        return schema


class CustomPagination(PageNumberPagination):
    page_size = 8

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "data": data,
            }
        )


def paginate_response(
    queryset,
    serializer_,
    request,
    page_size=10,
    paginator=CustomPagination,
    context=None,
):
    paginator_instance = paginator()
    paginator_instance.page_size = page_size
    if not context:
        context = {}
    return ResponseManager.handle_paginated_response(
        paginator_instance,
        serializer_(
            paginator_instance.paginate_queryset(queryset, request),
            many=True,
            context=context,
        ).data,
    )


def paginate_list(list_data, request, current_page=None, page_size=10):
    sliced_list = [
        list_data[i : page_size + i] for i in range(0, len(list_data) + 1, page_size)
    ]
    data = []
    current_page = 1 if current_page is None else int(current_page)

    if len(sliced_list) < current_page:
        data = ["number of page exceeds available data"]
    else:
        data = sliced_list[current_page - 1]

    return Response(
        {
            "count": len(list_data),
            "total_pages": len(sliced_list),
            "current_page": current_page,
            "data": data,
        }
    )


def paginate_list_to_dict(list_data, current_page=None, page_size=10):
    sliced_list = [
        list_data[i : page_size + i] for i in range(0, len(list_data) + 1, page_size)
    ]
    data = []
    current_page = 1 if current_page is None else int(current_page)

    if len(sliced_list) < current_page:
        data = ["number of page exceeds available data"]
    else:
        data = sliced_list[current_page - 1]

    return {
        "count": len(list_data),
        "total_pages": len(sliced_list),
        "current_page": current_page,
        "data": data,
    }
