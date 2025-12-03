from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    """
    Custom Django admin configuration for the Video model.
    Defines visible fields, marks some fields as read-only,
    and ensures that the thumbnail field is optional in the admin form.
    """
    fields = (
        'title', 
        'description', 
        'video_file', 
        'category',
        'thumbnail', 
        'hls_ready',
        'created_at',
    )
    
    readonly_fields = ('created_at', 'hls_ready',) 

    def get_form(self, request, obj=None, **kwargs):
        """
        Returns the admin form and adjusts field requirements.
        Ensures that 'thumbnail' is not required when creating or editing a Video.
        This prevents validation errors when no thumbnail is uploaded manually.
        """
        form = super().get_form(request, obj, **kwargs)
        
        if 'thumbnail' in form.base_fields:
            form.base_fields['thumbnail'].required = False
            
        return form

admin.site.register(Video, VideoAdmin)