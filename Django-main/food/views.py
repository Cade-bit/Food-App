from django.db.migrations import serializer
from django.shortcuts import render,redirect
from django.http import HttpResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle

from .models import Item
from django.template import loader
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse
from .serializers import ItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
import logging

# Other permissions that can be used are: IsAdminUser. IsAuthenticated, DjangoModelPermissions

logger = logging.getLogger(__name__)

# Create your views here.
#----------------------------> Creating view for index page
''' The following code implements separate caching based on the device the user is using 
@cache_page(60*15)
@vary_on_headers('User-Agent')
'''
# @cache_page(60*15)
def index(request):
    item_list = Item.objects.all()
    # Pagination
    paginator = Paginator(item_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'item_list': item_list,
        'page_obj': page_obj,
    }
    return render(request, 'food/index.html', context)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter, ]
    filterset_fields = ['item_name', 'item_price']
    ordering_fields = ['item_name', 'item_price']
    search_fields = ['item_name', 'item_description']
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    # def perform_create(self, serializer):
    #     serializer.save(user_name=self.request.user)


class ItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
#
# class ItemListCreateAPI(generics.ListCreateAPIView):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer


# class ItemListAPIView(APIView):
#     def get(self, request):
#         items = Item.objects.all()
#         serializer = ItemSerializer(items, many=True)
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = ItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)


class ItemDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return None
    def get(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({"Error": "Item not found"})
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    def put(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({"Error": "Item not found"})
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    def delete(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({"Error": "Item not found"})
        item.delete()
        return Response({"message": "Item deleted"})



# View and add items
# @api_view(["GET", "POST"])
# def item_list_api(request):
#     if request.method == "GET":
#         items = Item.objects.all()
#         serializer = ItemSerializer(items, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = ItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#
#
# @api_view(["GET", "PUT", "DELETE"])
# def item_detail_api(request, pk):
#     items = Item.objects.get(pk=pk)
#     if request.method == "GET":
#         serializer = ItemSerializer(items)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = ItemSerializer(items, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#     elif request.method == "DELETE":
#         items.delete()
#         return Response({"message": "Item deleted"})



# class IndexClassView(ListView):
#     logger.info("Fetching all items from the database")
#     logger.debug(f"Found {Item.objects.count()} items in the database")
#     model = Item
#     template_name = 'food/index.html'
#     context_object_name = 'item_list'

#------------------> Creating view for the details page
'''def item(request):
    return HttpResponse("<h1>This is an item view</h1>")

def detail(request, item_id):
    item = Item.objects.get(pk = item_id)
    context = {
        'item': item,
    }
    return render(request, 'food/details.html', context)'''

class FoodDetail(DetailView):
    logger.info(f"Fetching an item with the ID: {id} ")
    model = Item
    logger.debug(f"Item found {Item.item_name} ({Item.item_price})")
    template_name = 'food/details.html'
    context_object_name = 'item'

#------------------------> Add new item
'''def create_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('food:index')

    return render(request, 'food/item-form.html', {'form':form})'''

#---------------------> class based view for add items
class CreateItem( LoginRequiredMixin, CreateView):
    model = Item
    fields = ['item_name', 'item_description', 'item_price', 'item_image']
    template_name = 'food/item-form.html'

    def form_valid(self, form):
        form.instance.user_name = self.request.user

        return super().form_valid(form)


#-------------------------> Update item
class UpdateItem(UpdateView):
    model = Item
    fields = ['item_name', 'item_description', 'item_price', 'item_image']
    temple_name_suffix = '_update_form'

    def get_queryset(self):
        return Item.objects.filter(user_name = self.request.user)
#------------------------------> Delete an item
@login_required
def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)

    if request.method=="POST":
        item.delete()
        return redirect('food:index')

    return render(request, 'food/item-delete.html', {'item':item})


def get_objects(request):
    for item in Item.objects.all():
        print(item.item_name)

def get_objects_optimised(request):
    item = Item.objects.only('item_name')
    for item in item:
        print(item)