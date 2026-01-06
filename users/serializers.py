from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'get_full_name']


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    user_permissions = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    password = serializers.CharField(write_only=True)
    date_joined = serializers.DateTimeField(format='%d.%m.%Y %H:%M')

    class Meta:
        model = UserModel
        fields = ['id', 'email', 'first_name', 'last_name', 'date_joined', 'groups', 'user_permissions', 'is_staff',
                  'is_active', 'password']

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
