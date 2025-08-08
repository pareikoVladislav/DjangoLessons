from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.library.services.library import LibraryService
from src.users.dtos import CreateUserDTO, DetailedUserDTO


class LibraryStatistic(APIView):
    library_service = LibraryService()

    def get(self, request: Request) -> Response:
        query_params = request.query_params
        result = self.library_service.get_statistic_by_library(query_params)

        return Response(
            data=result,
            status=status.HTTP_200_OK
        )


class CreateLibraryMembers(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        service = LibraryService()
        library_id = kwargs.get("library_id")

        users_data = request.data.get("users", [])
        serializer = CreateUserDTO(data=users_data, many=True)
        serializer.is_valid(raise_exception=True)

        try:
            created_members = service.create_new_members(
                library_id=library_id,
                user_data_list=serializer.validated_data
            )
            response_serializer = DetailedUserDTO(created_members, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
