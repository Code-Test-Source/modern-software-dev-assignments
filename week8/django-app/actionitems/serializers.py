from rest_framework import serializers

from .models import ActionItem


class ActionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionItem
        fields = ["id", "description", "completed", "created_at"]
        read_only_fields = ["created_at"]
