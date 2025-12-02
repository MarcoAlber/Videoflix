from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    """
    Custom Django admin for the Video model.
    
    Displays different fields when adding a new video vs. editing an existing one.
    Sets certain fields as read-only.
    """
    fields_base = (
        'title', 
        'description', 
        'video_file', 
        'category',
    )
    
    fields_on_change = (
        'thumbnail',
        'hls_ready',
    )

    readonly_fields = ('created_at', 'hls_ready',) 

    def get_fields(self, request, obj=None):
        """
        Returns the fields to display in the admin form.
        
        - On creation (obj is None): show base fields only.
        - On editing (obj exists): show base fields plus additional fields.
        """
        if obj:
            return self.fields_base + self.fields_on_change
        else:
            return self.fields_base

admin.site.register(Video, VideoAdmin)