from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import ImgsPost
from .serializers import ImgsPostSerializer

# ImgsPost Views
@api_view(['GET', 'POST'])
def imgs_post_list(request):
    if request.method == 'GET':
        imgs = ImgsPost.objects.all()
        serializer = ImgsPostSerializer(imgs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ImgsPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def imgs_post_detail(request, img_id):
    img = get_object_or_404(ImgsPost, id=img_id)
    if request.method == 'GET':
        serializer = ImgsPostSerializer(img)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ImgsPostSerializer(img, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        img.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

