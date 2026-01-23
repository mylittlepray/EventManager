from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import EventImage
from .services import make_preview 

@receiver(post_save, sender=EventImage)
def generate_preview_on_save(sender, instance, created, **kwargs):
    """
    Автоматически создаёт превью для события, если его нет,
    при добавлении новой картинки.
    """
    if created:
        event = instance.event
        # Если у события ещё нет превью — генерируем из текущей картинки
        if not event.preview_image and instance.image:
            # Открываем картинку для чтения
            instance.image.open()
            preview_content = make_preview(instance.image.file)
            
            # Сохраняем в поле preview_image модели Event
            event.preview_image.save(
                f'preview_{event.id}.jpg',
                preview_content,
                save=True
            )

@receiver(post_delete, sender=EventImage)
def update_preview_on_delete(sender, instance, **kwargs):
    """
    Если удалили картинку, которая была превью, можно попробовать 
    поставить другую (опционально) или просто оставить как есть.
    """
    pass 
