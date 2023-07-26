from rest_framework import serializers
from .models import *



class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)





class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'

    def create(self, validated_data):
        user = UserAccount.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class DepartmentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'