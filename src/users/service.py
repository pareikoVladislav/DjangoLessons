from src.users.repository import UserRepository
from src.shared.base_service_response import ServiceResponse, ErrorType
from src.users.dtos import ListUsersDTO, DetailedUserDTO


class UserService:
    repository = UserRepository()

    def get_all_users(self):
        try:
            data = self.repository.get_all()

            serializer = ListUsersDTO(data, many=True)

            return ServiceResponse(
                success=True,
                data=serializer.data
            )
        except Exception as e:
            return ServiceResponse(
                success=False,
                message=f"Error retrieving users: {str(e)}",
                error_type=ErrorType.UNKNOWN_ERROR
            )

    def get_user_by_id(self, user_id: int):
        try:
            user = self.repository.get_by_id(user_id)

            if user is None:
                return ServiceResponse(
                    success=False,
                    message=f"User with ID {user_id} not found",
                    error_type=ErrorType.NOT_FOUND
                )

            serializer = DetailedUserDTO(user)

            return ServiceResponse(
                success=True,
                data=serializer.data
            )
        except Exception as e:
            return ServiceResponse(
                success=False,
                message=f"Error retrieving user: {str(e)}",
                error_type=ErrorType.UNKNOWN_ERROR
            )
