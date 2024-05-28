from django.db import models


class Form(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()
    date = models.DateField()
    occupation = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    """ __str__ method defines the string representation of the class instance
    exmaple-
    class Xyz(models.Model):
        col_1 = models.CharField(max_length=80)
        col_2 = models.EmailField()
        col_3 = models.DateField()

        def __str__(self):
            return "instance string representation"
            
    demo=Xyz()
    print(demo)
    
    output = instance string representation
    
    """


