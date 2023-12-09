from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from . import models
from ..base.services import delete_of_file
from apps.music.serializers import MusicSerializer
from ..music.models import Music


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    update_to = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.Profile
        fields = ('id', 'avatar', 'description', 'gender', 'update_to', 'user')

    def update(self, instance, validated_data):
        delete_of_file(instance.avatar.path)
        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Favorite
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # If content type is equal to music
        if data['content_type'] == 10:
            # Assuming data["object_id"] is the primary key of a Music instance
            music_instance = Music.objects.get(pk=data["object_id"])
            data['music'] = MusicSerializer(instance=music_instance, many=False).data
            data['music']['image'] = self.context['request'].build_absolute_uri(data['music']['image'])

        return data


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(
        allow_null=False,
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        allow_null=False,
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'email', 'profile')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserCRUDSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile')


class GoogleAuthSerializer(serializers.Serializer):
    """ Google Data Serialization
    """
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
