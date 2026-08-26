from . import views
from django.urls import path


app_name = 'food'
urlpatterns = [
    # URL pattern of API built with DRF
    path('api/items', views.ItemListCreateAPI.as_view(), name='item_list_api'),
    # URL pattern for single item
    path('api/items/<int:pk>', views.ItemRetrieveUpdateDestroyAPIView.as_view(), name='item_detail_api'),
    # URL Patterns of Django App
    #/food/ ----> This is the index page
    path('', views.IndexClassView.as_view(), name='index'),
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