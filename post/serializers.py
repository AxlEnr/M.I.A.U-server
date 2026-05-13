from rest_framework import serializers
from .models import Post
from pet.serializers import PetSerializer
from imgspost.serializers import ImgsPostSerializer
from user.models import User

class PostSerializer(serializers.ModelSerializer):
    pet = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    user_name = serializers.SerializerMethodField(read_only=True)
    user_profile_photo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'description', 'postDate', 'state', 'city',
            'petId', 'userId', 'pet', 'images', 'user_name', 'user_profile_photo'
        ]

    def get_pet(self, obj):
        from pet.models import Pet
        try:
            pet = Pet.objects.get(id=obj.petId_id)
            return PetSerializer(pet, context=self.context).data
        except Pet.DoesNotExist:
            return None

    def get_images(self, obj):
        from imgspost.models import ImgsPost
        images = ImgsPost.objects.filter(idPost=obj).order_by('-id')
        return ImgsPostSerializer(images, many=True, context=self.context).data

    def get_user_name(self, obj):
        if obj.userId:
            return f"{obj.userId.name} {obj.userId.first_name}".strip()
        return ""

    def get_user_profile_photo(self, obj):
        request = self.context.get('request')
        if obj.userId:
            profile = getattr(obj.userId, 'user_profile', None)
            if profile and profile.profilePhoto:
                url = profile.profilePhoto.url
                if request:
                    return request.build_absolute_uri(url)
                return url
        return None
