from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'profile_pic',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


# class LoginSerializer(serializers.Serializer):
#     email = serializers.CharField(required=True)
#     password = serializers.CharField(required=True)

#     class Meta:
#         fields = (
#             'email',
#             'password'
#         )

#     def validate(self, data):
#         """
#         Validates user data.
#         """
#         email = data.get('email', None)
#         password = data.get('password', None)

#         if email is None:
#             raise serializers.ValidationError(
#                 'An email address is required to log in.'
#             )

#         if password is None:
#             raise serializers.ValidationError(
#                 'A password is required to log in.'
#             )

#         user = authenticate(username=email, password=password)

#         if user is None:
#             raise serializers.ValidationError(
#                 'A user with this email and password was not found.'
#             )

#         return data
