from rest_framework import serializers
from .models import Category, Payment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields =['amount', 'payment_method', 'card_number', 'expiry_date', 'name']