try:
    from django.utils.http import urlsafe_base64_decode as uid_decoder
except:
    # make compatible with django 1.5
    from django.utils.http import base36_to_int as uid_decoder

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions

from ..utils import user_has_rights_on_share
from ..models import Share

class UpdateShareSerializer(serializers.Serializer):

    share_id = serializers.UUIDField(required=True)
    data = serializers.CharField(required=False)
    data_nonce = serializers.CharField(required=False, max_length=64)

    def validate(self, attrs):

        share_id = attrs.get('share_id')

        try:
            share = Share.objects.get(pk=share_id)
        except Share.DoesNotExist:
            msg = _("You don't have permission to access or it does not exist.")
            raise exceptions.ValidationError(msg)

        # check permissions on share
        if not user_has_rights_on_share(self.context['request'].user.id, share_id, write=True):
            msg = _("You don't have permission to access or it does not exist.")
            raise exceptions.ValidationError(msg)


        attrs['share'] = share
        attrs['data'] = attrs.get('data', False)
        attrs['data_nonce'] = attrs.get('data_nonce', False)

        return attrs