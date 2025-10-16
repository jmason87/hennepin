from rest_framework import generics, status
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer

class ItemList(generics.ListAPIView):
    queryset = Item.objects.order_by('created_at')
    serializer_class = ItemSerializer

    def get(self):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

class ItemCreate(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)