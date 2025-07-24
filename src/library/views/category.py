
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from src.library.models import Category
from src.library.serializers import CategorySerializer


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title']


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'title'



# from rest_framework.decorators import api_view
# from rest_framework.request import Request
# from rest_framework.response import Response
# from rest_framework import status

#
# @api_view(['GET'])
# def get_all_categories(request: Request) -> Response:
#     response = Category.objects.all()
#
#     serializer = CategorySerializer(
#         response,
#         many=True
#     )
#
#     return Response(
#         data=serializer.data,
#         status=status.HTTP_200_OK
#     )
#
#
# @api_view(['POST'])
# def create_new_category(request: Request) -> Response:
#     raw_data = request.data # RAW JSON DATA FROM FORM | RAW JSON
#
#     serializer = CategorySerializer(data=raw_data)
#
#     if serializer.is_valid():
#         serializer.save()
#
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_201_CREATED
#         )
#     return Response(
#         data=serializer.errors,
#         status=status.HTTP_400_BAD_REQUEST
#     )
