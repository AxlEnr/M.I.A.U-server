from rest_framework import serializers
from .models import ImgsPost

class ImgsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImgsPost
        fields = ['id', 'imgURL', 'idPost']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.imgURL:
            request = self.context.get('request')
            file_url = instance.imgURL.url
            if request:
                data['imgURL'] = request.build_absolute_uri(file_url)
            else:
                data['imgURL'] = file_url
        return data
