from django.urls import path
from . import views

urlpatterns = [
    path('', views.Menulist.as_view(), name='home'),
    path('item/<int:pk>/', views.MenuItemDetail.as_view(), name="menu_item")
    # int:pk was added as multiple menu items will use the link
    # thus to make it unique that menu item's primary key (pk) was used . pk is automatically a column ok database
]