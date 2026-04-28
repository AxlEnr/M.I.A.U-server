from rest_framework import serializers
from .models import ImgsPost

class ImgsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImgsPost
        fields = ['id', 'imgURL', 'idPost']

    def get_imgURL(self, obj):
        if obj.imgURL:
            request = self.context.get('request')
            url = obj.imgURL.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None