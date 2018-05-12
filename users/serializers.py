"""Serializers of users' app."""

from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for user model."""

    class Meta:
        """Meta settings."""

        model = User
        fields = ('username', 'email',)

    def create(self, validated_data):
        """Create user by validated data."""
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()

        return user