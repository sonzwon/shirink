from shortener.utils import *
from shortener.models import ShortenedUrls, Users, Statistic
from shortener.index.serializers import RegisterSerializer
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.http.response import Http404
from datetime import timedelta
from django.db.models.aggregates import Min, Count


class RegistertView(viewsets.ModelViewSet):
    queryset = User.objects.order_by("-created_at")
    serializer_class = RegisterSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        # POST METHOD
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            rtn = serializer.create(request, serializer.data)
            return Response(RegisterSerializer(rtn).data, status=status.HTTP_201_CREATED)