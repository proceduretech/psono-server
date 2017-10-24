from ..utils import user_has_rights_on_share

try:
    from django.utils.http import urlsafe_base64_decode as uid_decoder
except:
    # make compatible with django 1.5
    from django.utils.http import base36_to_int as uid_decoder

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions
from ..models import User_Share_Right, Group_Share_Right


class DeleteShareRightSerializer(serializers.Serializer):

    share_right_id = serializers.UUIDField(required=False) # Deprecated
    user_share_right_id = serializers.UUIDField(required=False)
    group_share_right_id = serializers.UUIDField(required=False)

    def validate(self, attrs):
        user_share_right_id = attrs.get('user_share_right_id', attrs.get('share_right_id', None))
        group_share_right_id = attrs.get('group_share_right_id', None)

        if user_share_right_id is None and group_share_right_id is None:
            msg = _("Either user or group share right needs to be specified.")
            raise exceptions.ValidationError(msg)

        if user_share_right_id is not None and group_share_right_id is not None:
            msg = _("Either user or group share right needs to be specified, not both")
            raise exceptions.ValidationError(msg)

        if user_share_right_id:
            # check if share_right exists
            try:
                share_right = User_Share_Right.objects.get(pk=user_share_right_id)
            except User_Share_Right.DoesNotExist:
                msg = _("You don't have permission to access or it does not exist.")
                raise exceptions.ValidationError(msg)
        else:
            # check if share_right exists
            try:
                share_right = Group_Share_Right.objects.get(pk=group_share_right_id)
            except Group_Share_Right.DoesNotExist:
                msg = _("You don't have permission to access or it does not exist.")
                raise exceptions.ValidationError(msg)


        # check permissions on parent
        if not user_has_rights_on_share(self.context['request'].user.id, share_right.share_id, grant=True):
            msg = _("You don't have permission to access or it does not exist.")
            raise exceptions.ValidationError(msg)

        attrs['share_right'] = share_right

        return attrs
