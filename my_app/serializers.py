from django.db.models import Q
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from my_app import models


class EmptySerializer(serializers.Serializer):
    pass


class InterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Interest
        fields = ["id", "sent_to", "sent_by", "is_accepted", "created_at"]
        extra_kwargs = {
            "sent_by": {"read_only": True},
            "is_accepted": {"read_only": True},
        }

    def validate_sent_to(self, data):
        request = self.context.get("request")
        already_exist = models.Interest.objects.filter(
            Q(sent_to=request.user, sent_by=data)
            | Q(sent_to=data, sent_by=request.user)
        ).exists()
        if already_exist:
            raise serializers.ValidationError("Already exist.")
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["sent_by"] = request.user
        return super().create(validated_data)


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = PhoneNumberField()


class MyInterestSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = models.Interest
        fields = ["id", "user", "created_at"]

    def get_user(self, data: models.Interest):
        request = self.context.get("request")
        user_id = request.user.id

        if data.sent_by.id != user_id:
            return UserSerializer(data.sent_by).data
        return UserSerializer(data.sent_to).data


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatMessage
        fields = ["id", "user", "interest", "message", "created_at"]
        extra_kwargs = {"user": {"read_only": True}, "interest": {"read_only": True}}

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        validated_data["interest_id"] = self.context.get("interest_id")
        return super().create(validated_data)
