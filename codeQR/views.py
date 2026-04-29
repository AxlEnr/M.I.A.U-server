import qrcode
import io
import base64
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files.base import ContentFile
from .models import CodeQR
from .serializers import CodeQRSerializer
from miau_backend.response import ApiResponse
import json

class CodeQRViewSet(viewsets.ModelViewSet):
    queryset = CodeQR.objects.all()
    serializer_class = CodeQRSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        return [permissions.AllowAny()]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data, status.HTTP_201_CREATED)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success('Código QR eliminado exitosamente', status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def generate_qr(self, request):
        pet_id = request.data.get('pet_id') or request.query_params.get('pet_id')
        if not pet_id:
            return ApiResponse.error("pet_id es requerido", status.HTTP_400_BAD_REQUEST)
        
        from pet.models import Pet
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return ApiResponse.error("Mascota no encontrada", status.HTTP_404_NOT_FOUND)

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        status_pet = pet.statusAdoption == 1 if 'Adoptado' else (
            pet.statusAdoption == 0 if 'Perdido' else 'Buscando Familia'
        )

        status_options = {0: 'Perdido', 1: 'Adoptado', 2: 'Buscando familia'} 
        status_pet = status_options.get(pet.statusAdoption, "Desconocido") 
        user = pet.userId

        data_to_encode = {
            "Nombre": pet.name,
            "Edad": pet.age,
            "Status": status_pet,
            "Nombre del Dueño": f"{user.name} {user.first_name}",
            "Email de contacto": user.email,
            "NOTA": "POR FAVOR SI ENCONTRÓ UNA MASCOTA EN LA CALLE CON ESTE QR, CONTACTE AL DUEÑO CUANTO ANTES A TRAVÉS DE SU CORREO O DE LA APP M.I.A.U"
        }

        qr.add_data(json.dumps(data_to_encode, ensure_ascii=False))
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        raw_bytes = buffer.getvalue()
        qr_code_base64 = base64.b64encode(raw_bytes).decode('utf-8')

        # Para la base de datos (Archivo real)
        data = ContentFile(raw_bytes, name=f'qr_pet_{pet.id}.png')

        # Para la respuesta JSON (String Base64)
        qr_code_data = f"data:image/png;base64,{qr_code_base64}"

        code_qr = CodeQR.objects.create(
            pet=pet,
            qr_image=data,
        )
        return ApiResponse.success({
            'qr_code': qr_code_data,
            'qr_id': code_qr.id,
            'pet_id': pet.id
        }, status.HTTP_201_CREATED)
