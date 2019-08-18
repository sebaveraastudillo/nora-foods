from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect

from .utils import get_url_base

from .forms import MenuForm, OptionForm, OrderForm
from .models import Menu, Option, Order
from .tasks import send_menu

class StaffRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        else:
            if not request.user.is_staff:
                return redirect(reverse_lazy('my_orders'))
            else:
                return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

class MenuListView(StaffRequiredMixin, ListView):
    model = Menu

class MenuCreateView(StaffRequiredMixin, CreateView):
    
    def get(self, request, *args, **kwargs):
        form = MenuForm()
        return render(request, 'menu/menu_form.html', {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        menu_list = Menu.objects.all()
        return render(request, 'menu/menu_list.html', {'menu_list':menu_list})

class MenuUpdateView(StaffRequiredMixin, UpdateView):
    model=Menu
    form_class=MenuForm
    template_name_suffix='_update_form'

    def get_success_url(self):
        return reverse_lazy('menu_update', args=[self.object.id]) + '?OK'

class OptionCreateView(StaffRequiredMixin, CreateView):
    model=Option
    form_class=OptionForm
    success_url=reverse_lazy('menu_create')

class OrderCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        menu = Menu.objects.filter(uuid=kwargs['menu_uuid'])
        if len(menu) > 0:
            form = OrderForm(initial = {'menu': menu[0]})
            return render(request, 'menu/order_form.html', {'form':form})
        else:
            return render(request, 'menu/error.html', {'message':'No existe un menu relacionado al UUID'})
    
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'menu/order_form.html', {'form':form, 'success': True})
        else:
            return render(request, 'menu/error.html', {'message':form.errors})

class OrderListView(StaffRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):
        menu = Menu.objects.filter(pk=kwargs['menu_id'])

        if len(menu) > 0:
            orders = Order.objects.filter(menu=menu[0])
            return render(request, 'menu/order_list.html', {'order_list': orders})
        else:
            return render(request, 'menu/error.html', {'message':'No existe el menu indicado'})

class OrderUserList(ListView):

    def get(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            orders = Order.objects.filter(user=request.user)
            return render(request, 'menu/order_list.html', {'order_list': orders})
        else:
            return redirect(reverse_lazy('login'))

def slack_send(request, menu_id):
    send_menu.delay(get_url_base(request), menu_id)
    response = redirect('/?OKSEND')
    return response