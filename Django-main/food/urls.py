from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.views.decorators.cache import cache_page, never_cache

from .views import ItemViewSet

router = DefaultRouter()
router.register(r'items', views.ItemViewSet, basename='item')


app_name = 'food'
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    # URL pattern of API built with DRF
    # path('api/items', views.ItemListCreateAPI.as_view(), name='item_list_api'),
    # URL pattern for single item
    # path('api/items/<int:pk>', views.ItemRetrieveUpdateDestroyAPIView.as_view(), name='item_detail_api'),
    # URL Patterns of Django App
    #/food/ ----> This is the index page
    # The bottom line of code is caching the url
    # path('', cache_page(60*15) (views.index), name='index'),
    # End
    path('', views.index, name='index'),
    #/food/(id of item) -----> This is the details page
    path('<int:pk>/', views.FoodDetail.as_view(), name='detail'),
    path('item/', views.FoodDetail.as_view(), name='item'),
    #Add items -------> This is for the add items page
    path('add', views.CreateItem.as_view(), name="create_item"),
    #Edit items -----> This is for the edit items page
    path('update/<int:item_id>/', views.UpdateItem.as_view(), name='update_item'),
    #delete item -----> This is for the delete items page
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
]