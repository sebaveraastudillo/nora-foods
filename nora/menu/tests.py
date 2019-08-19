from django.test import TestCase
from django.contrib.auth.models import User 
from .models import Menu, Option, Order
from .forms import MenuForm, OptionForm, OrderForm
from .tasks import send_menu
from nora.celery import app
from .utils import set_message_slack
from celery.contrib.testing.worker import start_worker

import datetime

# Create your tests here.
class MenuTestCase(TestCase):
    def setUp(self):
        self.option1 = Option.objects.create(name='Pure con pescado frito')
        self.option2 = Option.objects.create(name='Pastel de choclo')
        self.menu = Menu.objects.create(date=datetime.datetime.now())
        self.form_menu = MenuForm(data={'date': datetime.datetime.now(), 'options': [self.option1, self.option2]})
        
    def test_add_options_to_menu(self):
        """
        Check that the options were added to the menu
        """
        self.menu.options.add(self.option1, self.option2)
        self.assertEqual(len(self.menu.options.all()), 2)

    def test_create_menu(self):
        """
        check the creation of a menu
        """
        menu1 = Menu.objects.create(date=datetime.datetime.now() + datetime.timedelta(days=1))
        menu2 = Menu.objects.create(date=datetime.datetime.now() + datetime.timedelta(days=2))
        option3 = Option.objects.create(name='Arroz con Pollo al jugo')

        self.menu.options.add(self.option1, self.option2)
        menu2.options.add(option3)
        
        self.assertEqual(len(Menu.objects.all()), 3)

    def test_create_menu_without_date(self):
        """
        check the creation of a menu without a date
        """
        menu1 = Menu.objects.create()
        self.assertEqual(len(Menu.objects.all()), 2)

    def test_form_create_update_menu_valid(self):
        """
        check a valid form to create or update a menu
        """
        self.assertTrue(self.form_menu.is_valid())

    def test_form_create_update_menu_invalid(self):
        """
        check a invalid form to create or update a menu
        """
        form_menu = MenuForm()
        self.assertFalse(form_menu.is_valid())

class OptionTestCase(TestCase):
    def setUp(self):
        self.option = Option.objects.create(name='Pollo con arroz')
        self.form_option = OptionForm(data={'name': 'Pollo con arroz'})

    def test_check_create_option(self):
        """
        check the creation of a option
        """
        self.assertEqual(len(Option.objects.all()), 1)

    def test_form_create_option_valid(self):
        """
        check a valid form to create a option
        """
        self.assertTrue(self.form_option.is_valid())

    def test_form_create_option_invalid(self):
        """
        check a invalid form to create a option
        """
        form_option = OptionForm()
        self.assertFalse(form_option.is_valid())

class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user1', None, 'test12345')
        self.option = Option.objects.create(name='Pure con pescado frito')
        self.menu = Menu.objects.create(date=datetime.datetime.now())
        self.menu.options.add(self.option)
        self.order = Order.objects.create(menu=self.menu, option=self.option, user=self.user, customizations='Pescado sin espinas')

        self.form_order = OrderForm(initial = {'menu': self.menu}, data={'menu': self.menu.id, 'option': self.option.id, 'user': self.user.id, 'customizations':'Pescado sin espinas'}, )

    def test_create_order(self):
        """
        check the creation of a order
        """
        self.assertEqual(len(Order.objects.all()), 1)   

    def test_create_order_without_customizations(self):
        """
        check the creation of a order without customizations
        """
        order = Order.objects.create(menu=self.menu, option=self.option, user=self.user)
        self.assertEqual(len(Order.objects.all()), 2)

    def test_form_order_valid(self):
        """
        check a valid form to create a order
        """
        self.assertTrue(self.form_order.is_valid())
    
    def test_form_order_invalid(self):
        """
        check a invalid form to create a order
        """
        form_order = OrderForm()
        self.assertFalse(form_order.is_valid())

    def test_form_order_with_option_not_in_menu_options(self):
        """
        check a form order with a option that not in menu options
        """
        option = Option.objects.create(name='Arroz con pollo')
        form_order = OrderForm(initial = {'menu': self.menu}, data={'menu': self.menu.id, 'option': option.id, 'user': self.user.id, 'customizations':'Pescado sin espinas'}, )
        self.assertFalse(form_order.is_valid())