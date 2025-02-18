from rest_framework import serializers
from .models import DoctorHisob, DoctorTajriba

class DoctorHisobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorHisob
        fields = '__all__'

class DoctorTajribaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorTajriba
        fields = '__all__'
