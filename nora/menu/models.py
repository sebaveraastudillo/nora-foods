from django.db import models
import uuid
from django.contrib.auth.models import User

class Option(models.Model):
    """
    A class used to represent the Option objects

    Attributes
    ----------
    name : str
        name of the option
    created : datetime
        creation date
    updated : str
        updated date

    Methods
    -------
    __str__(self)
        returns the attribute that will be shown in the lists of the objects
    """
    name = models.CharField(max_length=200, verbose_name="Nombre", null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Opción"
        verbose_name_plural = "Opciones"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class Menu(models.Model):
    """
    A class used to represent the Menu objects

    Attributes
    ----------
    date : date
        date of the menu
    options: Option
        option objects related to
    uuid:
        uuid code of the menu
    created : datetime
        creation date
    updated : str
        updated date

    Methods
    -------
    __str__(self)
        returns the attribute that will be shown in the lists of the objects
    
    get_year(self)
        returns the year of the attribute date

    get_month(self)
        returns the month of the attribute date

    get_day(self)
        returns the day of the attribute date   
    """

    date = models.DateField(verbose_name="Fecha", null=True, blank=True)
    options = models.ManyToManyField(Option, verbose_name="Opciones")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return 'Menu ' + str(self.date)

    def get_year(self):
        return self.date.strftime('%Y')

    def get_month(self):
        return self.date.strftime('%m')

    def get_day(self):
        return self.date.strftime('%d')

class Order(models.Model):

    """
    A class used to represent the Order objects

    Attributes
    ----------
    menu : Menu
        menu related to order
    option: Option
        option object related to order
    user:
        user related to order
    customizations:
        customizations of the order user    
    created : datetime
        creation date
    updated : str
        updated date
    """

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="Menu")
    option = models.ForeignKey(Option, on_delete=models.CASCADE, verbose_name="Opción")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Empleado", null=True)
    customizations = models.TextField(verbose_name="Personalizaciones", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["created"]