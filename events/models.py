# Create your models here.
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q, F

from venues.models import Venue


class EventStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    SCHEDULED = "SCHEDULED", "Scheduled"
    PUBLISHED = "PUBLISHED", "Published"
    ENDED = "ENDED", "Ended"
    DELETED = "DELETED", "Deleted"


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    publish_at = models.DateTimeField(null=True, blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="events",
    )
    venue = models.ForeignKey(
        Venue,
        on_delete=models.PROTECT,
        related_name="events",
    )

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(25)],
        default=0,
    )

    status = models.CharField(
        max_length=16,
        choices=EventStatus.choices,
        default=EventStatus.DRAFT,
        db_index=True,
    )

    # Превью-изображение (позже сделаем автогенерацию 200px)
    preview_image = models.ImageField(
        upload_to="events/previews/",
        null=True,
        blank=True,
        editable=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(rating__gte=0) & Q(rating__lte=25),
                name="event_rating_0_25",
            ),
            models.CheckConstraint(
                condition=Q(end_at__gt=F("start_at")),
                name="event_end_after_start",
            ),
        ]

    def __str__(self):
        return self.title


class EventImage(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="events/images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for event_id={self.event_id}"
