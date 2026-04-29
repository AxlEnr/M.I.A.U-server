from rest_framework import serializers
from .models import Pet

class PetSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    qrId = serializers.SerializerMethodField()
    qrUrl = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'age', 'breed', 'size', 
            'petDetails', 'userId', 'statusAdoption', 
            'image', 'qrId', 'qrUrl'
        ]

    def get_qrId(self, obj):
        try:
            qr = obj.qr 
            return qr.id if qr else None
        except:
            return None
    
    def get_qrUrl(self, obj):
        try:
            qr = obj.qr
            if qr and hasattr(qr, 'qr_image') and qr.qr_image:
                request = self.context.get('request')
                if request is not None:
                    return request.build_absolute_uri(qr.qr_image.url)
                return qr.qr_image.url
        except:
            return None
        return None