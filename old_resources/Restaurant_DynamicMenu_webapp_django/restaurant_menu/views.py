from django.shortcuts import render
from django.views import generic
from .models import Item, MEAL_TYPE
#we will be creating class based views

class Menulist(generic.ListView):
    #queryset is a variable that stores the list of dtata
    queryset= Item.objects.order_by("-date_created")

    template_name = "index.html"
    # class based views ke liye return render template not needed

    """You can send python data to your .html using context
    get_context_data ia a function of ListView class of django
    within that function you write the context
    
    basically context is a dictionary whose keys and values can be accessed in the .html files using jinja 2 coding
    
    {{ item 1 }} will write Pizza on webpage"""



    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        # super() calls the parent class - Listview and we are getting some default values from the parent class

        context["meals"]= MEAL_TYPE
        # creates a key item 'menu' whose value is the tuple MEAL_TYPE

        return context
class MenuItemDetail(generic.DetailView):
    model = Item # Item is the class in models.py
    template_name = "menu_item_detail.html"


