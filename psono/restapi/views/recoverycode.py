from django.conf import settings
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from ..authentication import TokenAuthentication
from ..app_settings import (
    CreateRecoverycodeSerializer,
)
from ..models import (
    Recovery_Code
)

# import the logging
import logging
logger = logging.getLogger(__name__)


class RecoveryCodeView(GenericAPIView):

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def put(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):

        serializer = CreateRecoverycodeSerializer(data=request.data, context=self.get_serializer_context())

        if not serializer.is_valid():

            if settings.LOGGING_AUDIT:
                logger.info({
                    'ip': request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')),
                    'request_method': request.META['REQUEST_METHOD'],
                    'request_url': request.META['PATH_INFO'],
                    'success': False,
                    'status': 'HTTP_400_BAD_REQUEST',
                    'event': 'CREATE_RECOVERY_CODE_ERROR',
                    'errors': serializer.errors,
                    'user': request.user.username
                })

            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        # delete existing Recovery Codes
        Recovery_Code.objects.filter(user=request.user).delete()

        recovery_code = Recovery_Code.objects.create(
            user = request.user,
            recovery_authkey = make_password(str(serializer.validated_data['recovery_authkey'])),
            recovery_data = str(serializer.validated_data['recovery_data']),
            recovery_data_nonce = serializer.validated_data['recovery_data_nonce'],
            recovery_sauce = str(serializer.validated_data['recovery_sauce']),
        )

        if settings.LOGGING_AUDIT:
            logger.info({
                'ip': request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')),
                'request_method': request.META['REQUEST_METHOD'],
                'request_url': request.META['PATH_INFO'],
                'success': True,
                'status': 'HTTP_200_OK',
                'event': 'CREATE_RECOVERY_CODE_SUCCESS',
                'user': request.user.username
            })

        return Response({
            'recovery_code_id': recovery_code.id
        }, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
