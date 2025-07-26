from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.library.services.library import LibraryService


class LibraryStatistic(APIView):
    library_service = LibraryService()

    def get(self, request: Request) -> Response:
        query_params = request.query_params
        result = self.library_service.get_statistic_by_library(query_params)

        return Response(
            data=result,
            status=status.HTTP_200_OK
        )
