from django.contrib.auth import get_user_model
from rest_framework import serializers

from subscriptions.models import Plan
from subscriptions.services.subscription import subscription_create

UserModel = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'get_full_name']


class UserListCreateSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    user_permissions = serializers.StringRelatedField(read_only=True, many=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    date_joined = serializers.DateTimeField(format='%d.%m.%Y %H:%M', read_only=True)
    plan = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Plan.objects.all())

    class Meta:
        model = UserModel
        fields = ['id', 'email', 'first_name', 'last_name', 'date_joined', 'groups', 'user_permissions', 'is_staff',
                  'is_active', 'password1', 'password2', 'plan']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Паролі не збігаються'})

        return data

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        del validated_data['password2']
        plan = validated_data.pop('plan')

        user = UserModel.objects.create_user(**validated_data)
        user.set_password(password1)
        user.save()

        subscription_create(user, plan)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'first_name', 'last_name']
