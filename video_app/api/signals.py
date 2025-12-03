# video_app/api/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import Video
import django_rq
from video_app.api.tasks import generate_thumbnail, generate_hls 

@receiver(post_save, sender=Video)
def generate_thumbnail_and_hls_signal(sender, instance, created, **kwargs):
    """ 
    Signal-Handler, der Hintergrund-Tasks nach dem Speichern einer Video-Instanz auslöst.
    
    - Bei Erstellung wird HLS-Generierung gestartet.
    - Die Thumbnail-Generierung wird NUR gestartet, wenn KEIN Thumbnail 
      vom Benutzer hochgeladen wurde.
    """
    if created and instance.video_file:
        queue = django_rq.get_queue("default")
        
        # 1. Bedingte Thumbnail-Generierung
        # Prüfe, ob das 'thumbnail'-Feld der Instanz leer ist.
        # Wenn KEIN Thumbnail hochgeladen wurde, generiere eins.
        if not instance.thumbnail:
            queue.enqueue(generate_thumbnail, instance.id)
        
        # 2. HLS-Generierung (wie bisher)
        queue.enqueue(generate_hls, instance.id)