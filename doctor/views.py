from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DoctorHisob, DoctorTajriba
from .serializers import DoctorHisobSerializer, DoctorTajribaSerializer

@api_view(['GET', 'POST'])
def doctor_hisob_list(request):
    """
    DoctorHisob ro'yxatiga yangi yozuv qo'shish yoki mavjudlarini ko'rsatish.
    """
    if request.method == 'GET':
        doctor_hisoblar = DoctorHisob.objects.all()
        serializer = DoctorHisobSerializer(doctor_hisoblar, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DoctorHisobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def doctor_tajriba_list(request):
    """
    DoctorTajriba ro'yxatiga yangi yozuv qo'shish yoki mavjudlarini ko'rsatish.
    """
    if request.method == 'GET':
        doctor_tajribalar = DoctorTajriba.objects.all()
        serializer = DoctorTajribaSerializer(doctor_tajribalar, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DoctorTajribaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
