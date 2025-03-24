# views.py (dentro de la aplicación pet)

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication  # Importación agregada
from rest_framework.permissions import IsAuthenticated
from .models import Pet
from codeQR.models import CodeQR
from .serializers import PetSerializer
from codeQR.serializer import CodeQRSerializer 
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.files.storage import default_storage
import qrcode
from io import BytesIO
from reportlab.pdfgen import canvas
import os

# Vista para listar y crear mascotas
# Vista para listar mascotas
# Vista para listar mascotas
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def pet_list(request):
    pets = Pet.objects.filter(userId=request.user).select_related("qrId")
    data = []

    for pet in pets:
        pet_data = PetSerializer(pet).data
        if pet.qrId:
            pet_data['qrCode'] = {
                "id": pet.qrId.id,  # ID del QR
                "qr_code_url": pet.qrId.qr_code_url  # URL del QR
            }
        else:
            pet_data['qrCode'] = None  # No hay QR generado aún

        data.append(pet_data)

    return Response(data)
      
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

# Vista para generar un código QR para una mascota
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def generate_qr_for_pet(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id, userId=request.user)  # Obtener la mascota del usuario logueado
    except Pet.DoesNotExist:
        return Response({"error": "Mascota no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    # Crear el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f" Nombre de la mascota: {pet.name} \n Nombre del Dueño: {request.user.name} \n Contacto: {request.user.phone_number}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar la imagen del QR en un archivo temporal
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_image_path = os.path.join(settings.MEDIA_ROOT, f"qr_{pet.id}.png")
    with open(qr_image_path, "wb") as f:
        f.write(buffer.getvalue())

    # Crear un PDF con el código QR
    pdf_path = os.path.join(settings.MEDIA_ROOT, f"qr_{pet.id}.pdf")
    c = canvas.Canvas(pdf_path)
    c.drawImage(qr_image_path, 100, 700, width=200, height=200)
    c.drawString(100, 680, f"Pet ID: {pet.id}")
    c.drawString(100, 660, f"Name: {pet.name}")
    c.drawString(100, 640, f"Owner: {request.user.email}")
    c.save()

    # Guardar la ruta del PDF en la base de datos
    qr_code = CodeQR.objects.create(
        qr_code_url=qr_image_path,
        pdf_url=pdf_path,
    )
    pet.qrId = qr_code
    pet.save()

    # Devolver la respuesta con la ruta del PDF
    return Response({
        "qr_code_url": qr_image_path,
        "pdf_url": pdf_path,
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def report_lost_pet(request):
    data = request.data.copy()
    data['userId'] = request.user.id  # Asignar el ID del usuario autenticado
    data['qrId'] = 1  # Asignar un código QR por defecto (ajusta esto según tu lógica)
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

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Pet
from .serializers import PetSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  # Cambiar a JWT

# Vista para listar y crear mascotas
# Vista para listar y crear mascotas
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])  # Usar JWTAuthentication
@permission_classes([IsAuthenticated])
def pet_list(request):
    if request.method == 'GET':
        # Filtrar mascotas por el usuario autenticado
        pets = Pet.objects.filter(userId=request.user)  # Solo mascotas del usuario logueado
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

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_qr(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id, userId=request.user)
        if pet.qrId:
            pet.qrId.delete()  # Eliminar el QR asociado
            pet.qrId = None
            pet.save()
            return Response({'message': 'QR eliminado correctamente'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No hay QR para eliminar'}, status=status.HTTP_400_BAD_REQUEST)
    except Pet.DoesNotExist:
        return Response({'error': 'Mascota no encontrada'}, status=status.HTTP_404_NOT_FOUND)