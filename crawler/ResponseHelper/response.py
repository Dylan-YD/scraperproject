from django.http import JsonResponse
from rest_framework import status

#response helper with message and status code
class ResponseHelper:
    @staticmethod
    def get_success_response(data, message):
        return JsonResponse({"status":200,"data" : data,"message": message}, status=status.HTTP_200_OK)

    @staticmethod
    def get_bad_request_response(message):
        return JsonResponse({"status": 400, 'message': message}, status = status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_not_found_response(message):
        return JsonResponse({'status': 404, 'message': message}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_unauthorized_response(message):
        return JsonResponse({'status': 401, 'message': message}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def get_forbidden_response(message):
        return JsonResponse({'status': 403, 'message': message}, status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def get_internal_server_error_response(message):
        return JsonResponse({'status': 500, 'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @staticmethod
    def get_unprocessable_entity_response(message):
        return JsonResponse({'status': 422, 'message': message}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @staticmethod
    def get_conflict_response(message):
        return JsonResponse({'status': 409, 'message': message}, status=status.HTTP_409_CONFLICT)

    @staticmethod
    def get_created_response( data, message):
        return JsonResponse({'status': 201,'data':data, 'message': message}, status=status.HTTP_201_CREATED)

    @staticmethod
    def get_precondition_failed_response(message):
        return JsonResponse({'status': 412, 'message': message}, status=status.HTTP_412_PRECONDITION_FAILED)

    @staticmethod
    def get_method_not_allowed_response(message):
        return JsonResponse({'status': 405, 'message': message}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @staticmethod
    def get_not_acceptable_response(message):
        return JsonResponse({'status': 406, 'message': message}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def get_request_timeout_response(message):
        return JsonResponse({'status': 408, 'message': message}, status=status.HTTP_408_REQUEST_TIMEOUT)