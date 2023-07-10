from django.contrib.auth.models import User
from facts.models import Fact
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'is_staff',
                   'is_active', 'date_joined', 'groups', 'user_permissions')


class FactSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Fact
        fields = '__all__'
        depth = 1
