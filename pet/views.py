from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Pet
from .serializers import PetSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  # Cambiar a JWT

# Vista para listar y crear mascotas
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])  # Usar JWTAuthentication
@permission_classes([IsAuthenticated])
def pet_list(request):
    if request.method == 'GET':
        # Filtrar mascotas por el usuario autenticado
        pets = Pet.objects.all()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Asignar el usuario autenticado y un código QR por defecto
        data = request.data.copy()
        data['userId'] = request.user.id  # Asignar el ID del usuario autenticado
        data['qrId'] = 1  # Asignar un código QR por defecto (ajusta esto según tu lógica)

        serializer = PetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para obtener, actualizar o eliminar una mascota por ID
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])  # Usar JWTAuthentication
@permission_classes([IsAuthenticated])
def pet_detail(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id, userId=request.user)  # Asegurar que la mascota pertenezca al usuario
    except Pet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PetSerializer(pet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#vista para listar mascotas en adopcion y perdidas:
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def pet_list_filtered(request):
    status_filter = request.query_params.get('status', None)
    pets = Pet.objects.all()

    if status_filter is not None:
        pets = pets.filter(statusAdoption=status_filter)

    serializer = PetSerializer(pets, many=True)
    return Response(serializer.data)

#vista para reportar mascotas perdiadas
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def report_lost_pet(request):
    data = request.data.copy()
    data['userId'] = request.user.id
    data['qrId'] = 1  # Asignar un código QR por defecto
    data['statusAdoption'] = 0  # Estado LOST

    serializer = PetSerializer(data=data)
    if serializer.is_valid():
        pet = serializer.save()

        # Crear un post asociado a la mascota perdida
        post_data = {
            'title': f"Mascota perdida: {pet.name}",
            'description': request.data.get('description', ''),
            'postDate': timezone.now().date(),
            'petId': pet.id,
            'userId': request.user.id,
        }
        post_serializer = PostSerializer(data=post_data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#vista para publicar mascotas en adopcion
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def publish_adoption_pet(request):
    data = request.data.copy()
    data['userId'] = request.user.id
    data['qrId'] = 1  # Asignar un código QR por defecto
    data['statusAdoption'] = 2  # Estado LOOKING

    serializer = PetSerializer(data=data)
    if serializer.is_valid():
        pet = serializer.save()

        # Crear un post asociado a la mascota en adopción
        post_data = {
            'title': f"Mascota en adopción: {pet.name}",
            'description': request.data.get('description', ''),
            'postDate': timezone.now().date(),
            'petId': pet.id,
            'userId': request.user.id,
        }
        post_serializer = PostSerializer(data=post_data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)