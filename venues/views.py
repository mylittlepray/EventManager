# venues/views.py
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse

from core.permissions import IsSuperUser
from .models import Venue
from .serializers import VenueSerializer

@extend_schema_view(
    list=extend_schema(
        tags=["Площадки"],
        summary="Список площадок",
        description="Возвращает список площадок (мест проведения). Доступно только суперпользователю.",
        responses={
            200: OpenApiResponse(response=VenueSerializer(many=True), description="Список площадок."),
            403: OpenApiResponse(description="Только для superuser."),
        },
    ),
    retrieve=extend_schema(
        tags=["Площадки"],
        summary="Детали площадки",
        description="Возвращает одну площадку по её id. Доступно только суперпользователю.",
        responses={
            200: OpenApiResponse(response=VenueSerializer, description="Площадка."),
            403: OpenApiResponse(description="Только для superuser."),
            404: OpenApiResponse(description="Площадка не найдена."),
        },
    ),
    create=extend_schema(
        tags=["Площадки"],
        summary="Создать площадку",
        description="Создаёт площадку. Доступно только суперпользователю.",
        responses={
            201: OpenApiResponse(response=VenueSerializer, description="Площадка создана."),
            400: OpenApiResponse(description="Ошибка валидации."),
            403: OpenApiResponse(description="Только для superuser."),
        },
    ),
    update=extend_schema(
        tags=["Площадки"],
        summary="Обновить площадку",
        description="Полное обновление площадки (PUT). Доступно только суперпользователю.",
        responses={
            200: OpenApiResponse(response=VenueSerializer, description="Площадка обновлена."),
            400: OpenApiResponse(description="Ошибка валидации."),
            403: OpenApiResponse(description="Только для superuser."),
            404: OpenApiResponse(description="Площадка не найдена."),
        },
    ),
    partial_update=extend_schema(
        tags=["Площадки"],
        summary="Частично обновить площадку",
        description="Частичное обновление площадки (PATCH). Доступно только суперпользователю.",
        responses={
            200: OpenApiResponse(response=VenueSerializer, description="Площадка обновлена."),
            400: OpenApiResponse(description="Ошибка валидации."),
            403: OpenApiResponse(description="Только для superuser."),
            404: OpenApiResponse(description="Площадка не найдена."),
        },
    ),
    destroy=extend_schema(
        tags=["Площадки"],
        summary="Удалить площадку",
        description="Удаляет площадку. Доступно только суперпользователю.",
        responses={
            204: OpenApiResponse(description="Площадка удалена."),
            403: OpenApiResponse(description="Только для superuser."),
            404: OpenApiResponse(description="Площадка не найдена."),
        },
    ),
)
class VenueViewSet(ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsSuperUser]
