from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from main.models import *
from main.serializers import *

# Create your views here.
class indexViewSet(viewsets.ModelViewSet):
    queryset = daily.objects.all()
    serializer_class = dailySerializer
    # new view
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly,
     #                     IsOwnerOrReadOnly]

    #@action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    #def highlight(self, request, *args, **kwargs):
     #   snippet = self.get_object()
      #  return Response(snippet.highlighted)

    #def perform_create(self, serializer):
    #    serializer.save(owner=self.request.user)
