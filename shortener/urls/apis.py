from shortener.models import ShortenedUrls, Users
from shortener.urls.serializers import UrlListSerializer, UrlCreateSerializer
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response


class UrlListView(viewsets.ModelViewSet):
    queryset = ShortenedUrls.objects.order_by("-created_at")
    serializer_class = UrlListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        """POST METHOD"""
        serializer = UrlCreateSerializer(data=request.data)
        if serializer.is_valid():
            rtn = serializer.create(request, serializer.data)
            return Response(UrlListSerializer(rtn).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """DETAIL GET"""
        pass

    def update(self, request, pk=None):
        """PUT METHOD"""
        pass

    def partial_update(self, request, pk=None):
        """PATCH METHOD"""
        pass

    def destroy(self, request, pk=None):
        """DELETE METHOD"""
        pass

    def list(self, request):
        """GET ALL"""
        pass
