from django.db import models
import uuid
from django.contrib.auth.models import User

class Option(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Opción"
        verbose_name_plural = "Opciones"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Menu(models.Model):
    date = models.DateField(verbose_name="Fecha", null=True, blank=True)
    options = models.ManyToManyField(Option, verbose_name="Opciones")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return 'Menu ' + str(self.date)

class Order(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="Menu")
    option = models.ForeignKey(Option, on_delete=models.CASCADE, verbose_name="Opción")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Empleado", null=True)
    customizations = models.TextField(verbose_name="Personalizaciones")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["created"]
