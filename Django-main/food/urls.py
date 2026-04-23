from . import views
from django.urls import path

app_name = 'food'
urlpatterns = [
    #/food/ ----> This is the index page
    path('', views.IndexClassView.as_view(), name='index'),
    #/food/(id of item) -----> This is the details page
    path('<int:pk>/', views.FoodDetail.as_view(), name='detail'),
    path('item/', views.FoodDetail.as_view(), name='item'),
    #Add items -------> This is for the add items page
    path('add', views.CreateItem.as_view(), name="create_item"),
    #Edit items -----> This is for the edit items page
    path('update/<int:item_id>/', views.update_item, name='update_item'),
    #delete item -----> This is for the delete items page
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
]