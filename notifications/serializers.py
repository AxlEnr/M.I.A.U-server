from rest_framework import serializers
from .models import Notifications

class NotificationsSerializer(serializers.ModelSerializer):
    related_post_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Notifications
        fields = ['id', 'notifType', 'message', 'read', 'notiDate', 'userId', 'related_post_id']
    
    def get_related_post_id(self, obj):
        return obj.related_post.id if obj.related_post else None