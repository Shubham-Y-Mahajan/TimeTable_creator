from django.db import models
from django.contrib.auth.models import User

MEAL_TYPE=(
    ("starters", "Starters"),
    ("salads", "Salads"),
    ("main_dishes", "Main Dishes")
    # first half used in backend code - in the actual database (db browser )
    # 2nd half displayed on front end - on the django admin interface while adding meals
    # example ("hulahul", "dessert") will show as meal type = dessert in django admin interface
    # but in the database table the meal type will be hulahul
    # this tuple indexing is done automarically
)
STATUS=(
    (0, "Unavailable"),
    (1, "Available")
)
class Item(models.Model):
    meal = models.CharField(max_length=1000, unique=True)
    description = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    meal_type = models.CharField(max_length=200,choices=MEAL_TYPE)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    """The 'USER' argument link the two databases - restaurant_menu and auth_user
    note: auth_user is django created"""
    # which cook created the dish vaghera
    #here we are creating a relation (many to one) between the User Table and Item table

    # if John is deleted from User then all his created meals will get deleted if we use cascade
    # The meals will not be deleted upon user deletion if we use PROTECT
    # The mels wil be assigned to NULL author if we us SET_NULL

    status = models.IntegerField(choices=STATUS, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meal
