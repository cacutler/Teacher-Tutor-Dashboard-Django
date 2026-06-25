from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Status

User = get_user_model()


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    """
    Read-focused serializer. Password is never exposed; statuses come back
    as nested objects so the frontend doesn't need a second round-trip.
    """
    statuses = StatusSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "middle_name", "birthdate", "gender", "is_staff", "is_active",
            "date_joined", "statuses",
        ]
        read_only_fields = ["id", "is_staff", "is_active", "date_joined"]


class UserWriteSerializer(serializers.ModelSerializer):
    """
    Use for create/update. Accepts statuses as a list of Status IDs and
    handles password hashing -- never assign request.data['password']
    straight onto the model.
    """
    password = serializers.CharField(write_only=True, required=False)
    statuses = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Status.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "middle_name", "birthdate", "gender", "statuses", "password",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        statuses = validated_data.pop("statuses", [])
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        if statuses:
            user.statuses.set(statuses)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        statuses = validated_data.pop("statuses", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        if statuses is not None:
            instance.statuses.set(statuses)
        return instance
