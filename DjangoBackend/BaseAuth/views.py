from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from BaseAuth.mixins import CustomMixins


class BaseAuthModelViewset(ModelViewSet, CustomMixins):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        params = self.request.query_params

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def extract_error_handler(self, err):
        if isinstance(err, dict):
            for key, value in err.items():
                if isinstance(value, list) and value:
                    return str(value[0])
                else:
                    return self.extract_error_handler(value)
        return str(err)


def custom_401(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, NotAuthenticated):
        return Response(
            {"error": "You are not authorized", "code": "NOT_ATHORIZED_401"}
        )
    return response
