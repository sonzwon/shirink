from shortener.utils import *
from shortener.models import ShortenedUrls, Users, Statistic, QrCode
from shortener.urls.serializers import (
    UrlListSerializer,
    UrlCreateSerializer,
    BrowerStatSerializer,
    QrListSerializer,
    QrCreateSerializer,
)
from django.contrib.auth.models import User, Group
from rest_framework.decorators import renderer_classes, action
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.http.response import Http404
from datetime import timedelta
from django.db.models.aggregates import Min, Count


class UrlListView(viewsets.ModelViewSet):
    queryset = ShortenedUrls.objects.order_by("-created_at")
    serializer_class = UrlListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        # POST METHOD
        serializer = UrlCreateSerializer(data=request.data)
        if serializer.is_valid():
            rtn = serializer.create(request, serializer.data)
            return Response(UrlListSerializer(rtn).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """DETAIL GET"""
        queryset = self.get_queryset().filter(pk=pk)
        serializer = UrlListSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """PUT METHOD"""
        pass

    def partial_update(self, request, pk=None):
        """PATCH METHOD"""
        pass

    @renderer_classes([JSONRenderer])
    def destroy(self, request, pk=None):
        """DELETE METHOD"""
        queryset = self.get_queryset().filter(pk=pk, creator_id=request.user.id)
        print(pk, request.user.id)
        if not queryset.exists():
            raise Http404
        queryset.delete()
        url_count_changer(request, False)
        return MsgOk()

    def list(self, request):
        """GET ALL"""
        queryset = self.get_queryset().filter(creator_id=request.user.id).all()
        serializer = UrlListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get", "post"])
    def add_browser_today(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk, creator_id=request.user.id).first()
        new_history = Statistic()
        new_history.record(request, queryset, {})
        return MsgOk

    @action(detail=True, methods=["get"])
    def get_browser_stats(self, request, pk=None):
        queryset = Statistic.objects.filter(shortened_url_id=pk, shortened_url__creator_id=request.user.id)

        if not queryset.exists():
            print("queryset is not exist")
            raise Http404

        browers = (
            queryset.values("web_browser", "created_at__date")
            .annotate(count=Count("id"))
            .values("count", "web_browser", "created_at__date")
            .order_by("-created_at__date")
        )
        print(browers)
        browers = (
            queryset.values("web_browser")
            .annotate(count=Count("id"))
            .values("count", "web_browser")
            .order_by("-count")
        )
        serializer = BrowerStatSerializer(browers, many=True)

        return Response(serializer.data)


class QrListView(viewsets.ModelViewSet):
    queryset = QrCode.objects.order_by("-created_at")
    serializer_class = QrListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        # POST METHOD
        serializer = QrCreateSerializer(data=request.data)
        if serializer.is_valid():
            rtn = serializer.create(request, serializer.data)
            return Response(QrListSerializer(rtn).data, status=status.HTTP_201_CREATED)
