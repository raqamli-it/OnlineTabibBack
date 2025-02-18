import json

from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from config import settings
from .models import Category, Payment
from .serializers import CategorySerializer, PaymentSerializer
from django.http import Http404, JsonResponse


# Category list view
class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

# Category detail view
class CategoryDetailView(APIView):
    def get_object(self, category_id):
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_id):
        category = self.get_object(category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)




class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        # Karta ma'lumotlarini tekshirish (oddiy validatsiya)
        if len(payment.card_number) != 16:
            payment.status = 'failed'
            payment.save()
            return Response({"error": "Karta raqami noto‘g‘ri"}, status=status.HTTP_400_BAD_REQUEST)

        # To‘lov tizimi bilan integratsiya qilish (Fake to‘lov)
        payment.status = 'success'
        payment.save()
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)






@csrf_exempt
def payme_callback(request):
    """Payme dan kelgan callback so‘rovni qabul qilish"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Payme callback data:", data)  # Debug uchun
            return JsonResponse({"status": "success", "message": "Payme to‘lov tasdiqlandi"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Yaroqsiz JSON"}, status=400)

    return JsonResponse({"status": "error", "message": "Faqat POST so‘rov qabul qilinadi"}, status=405)

@csrf_exempt
def click_callback(request):
    """Click dan kelgan callback so‘rovni qabul qilish"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Click callback data:", data)  # Debug uchun
            return JsonResponse({"status": "success", "message": "Click to‘lov tasdiqlandi"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Yaroqsiz JSON"}, status=400)

    return JsonResponse({"status": "error", "message": "Faqat POST so‘rov qabul qilinadi"}, status=405)