from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect

from .utils import set_message_slack, get_url_base

from .forms import MenuForm, OptionForm, OrderForm
from .models import Menu, Option, Order
from .tasks import send_menu

import datetime

class CheckAuthMixin(object):

    """
    A class used to check authentication

    Methods
    -------
    dispatch(self, request, *args, **kwargs)
        if user is staff (NORA) execute the action of CBV referenced, else reload the page my_orders
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        else:
            if not request.user.is_staff:
                return redirect(reverse_lazy('my_orders'))
            else:
                return super(CheckAuthMixin, self).dispatch(request, *args, **kwargs)

class MenuListView(CheckAuthMixin, ListView):
    """
    A class used to show the menu's list
    """
    model = Menu

class MenuCreateView(CheckAuthMixin, CreateView):
    
    """
    A class used to create a menu

    Methods
    -------
    get(self, request, *args, **kwargs)
        render the template with form to create a menu
    
    post(self, request, *args, **kwargs)
        create a menu with the form data
    """

    def get(self, request, *args, **kwargs):
        form = MenuForm()
        return render(request, 'menu/menu_form.html', {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        #render the menu list
        menu_list = Menu.objects.all()
        return render(request, 'menu/menu_list.html', {'menu_list':menu_list})

class MenuUpdateView(CheckAuthMixin, UpdateView):
    """
    A class used to update a menu

    Methods
    -------
    get_success_url(self)
        make a reverse_lay to menu_update url
    """
    model=Menu
    form_class=MenuForm
    template_name_suffix='_update_form'

    def get_success_url(self):
        return reverse_lazy('menu_update', args=[self.object.id]) + '?OK'

class OptionCreateView(CheckAuthMixin, CreateView):
    """
    A class used to create a option
    """
    model=Option
    form_class=OptionForm
    success_url=reverse_lazy('menu_create')

class OrderCreateView(CreateView):
    
    """
    A class used to create a order

    Methods
    -------
    get(self, request, *args, **kwargs)
        render the template with form to create a order if the actual moment is less than a date menu at 11 AM
    
    post(self, request, *args, **kwargs)
        create a order with the form data
    """
    def get(self, request, *args, **kwargs):
        menu = Menu.objects.filter(uuid=kwargs['menu_uuid'])
        if len(menu) > 0:
            
            #compare if now is greather than menu date at 11 AM
            if datetime.datetime(int(menu[0].get_year()), int(menu[0].get_month()), int(menu[0].get_day()), 11) > datetime.datetime.now():
                form = OrderForm(initial = {'menu': menu[0]})
                return render(request, 'menu/order_form.html', {'form':form})
            else:
                return render(request, 'menu/error.html', {'message':'Ya no se pueden realizar pedidos de este menu.'})    
        else:
            return render(request, 'menu/error.html', {'message':'No existe un menu relacionado al UUID'})
    
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'menu/order_form.html', {'form':form, 'success': True})
        else:
            return render(request, 'menu/error.html', {'message':form.errors})

class OrderListView(CheckAuthMixin, ListView):

    """
    A class used to show a order's list

    Methods
    -------
    get(self, request, *args, **kwargs)
        render the template with the list of orders
    
    """
    def get(self, request, *args, **kwargs):
        menu = Menu.objects.filter(pk=kwargs['menu_id'])

        if len(menu) > 0:
            orders = Order.objects.filter(menu=menu[0])
            return render(request, 'menu/order_list.html', {'order_list': orders})
        else:
            return render(request, 'menu/error.html', {'message':'No existe el menu indicado'})

class OrderUserList(ListView):

    """
    A class used to show a user's order list

    Methods
    -------
    get(self, request, *args, **kwargs)
        render the template with the list of orders
    
    """

    def get(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            orders = Order.objects.filter(user=request.user)
            return render(request, 'menu/order_list.html', {'order_list': orders})
        else:
            return redirect(reverse_lazy('login'))

def slack_send(request, menu_id):
    """
    Send the menu info to slack channel through a celery task
    """
    message=set_message_slack(menu_id, get_url_base(request))
    send_menu.apply_async(args=[message])
    response = redirect('/?OKSEND')
    return response