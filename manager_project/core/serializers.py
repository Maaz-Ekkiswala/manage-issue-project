from rest_framework import serializers

from manager_project.core.function import get_user_label


class BaseSerializer(serializers.ModelSerializer):
    created_ts = serializers.ReadOnlyField()
    updated_ts = serializers.ReadOnlyField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        try:
            if 'created_by' in ret.keys():
                ret['created_by'] = get_user_label(user=instance.created_by)
            if 'updated_by' in ret.keys():
                ret['updated_by'] = get_user_label(user=instance.updated_by)
        except Exception as ex:
            pass
        return ret

    def validate_serializer(self):
        if not self.is_valid():
            errors = dict(self.errors)
            field = list(errors.keys())[0]
            message = "%s - %s" % (field, errors[field][0])
            return (False, message)
        return (True, None)
