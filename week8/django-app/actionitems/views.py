from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ActionItem
from .serializers import ActionItemSerializer


class ActionItemViewSet(viewsets.ModelViewSet):
    queryset = ActionItem.objects.all()
    serializer_class = ActionItemSerializer

    @action(detail=True, methods=["put"])
    def complete(self, request, pk=None):
        item = self.get_object()
        item.completed = True
        item.save()
        return Response(self.get_serializer(item).data)
