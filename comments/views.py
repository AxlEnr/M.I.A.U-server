from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Comments
from .serializers import CommentsSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
# Comments Views
@api_view(['GET', 'POST'])
def comments_list(request):
    if request.method == 'GET':
        post_id = request.query_params.get('postId')
        if post_id:
            comments = Comments.objects.filter(postId=post_id)
        else:
            comments = Comments.objects.all()  # O puedes usar Comments.objects.none() si prefieres no mostrar nada sin filtro

        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def comments_detail(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    if request.method == 'GET':
        serializer = CommentsSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CommentsSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.request.query_params.get('postId')
        if post_id:
            return Comments.objects.filter(postId=post_id)
        return Comments.objects.none()  # Retornar vacío si no se pasa postId

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

