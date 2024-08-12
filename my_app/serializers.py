from django.db.models import Q
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
