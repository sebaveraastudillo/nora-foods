from .models import Menu

def get_url_base(request):
    """
    make the base url
    """
    if request.is_secure():
        protocol = 'https://'
    else:
        protocol = 'http://'

    return protocol + request.META['HTTP_HOST'] + '/'

def set_message_slack(menu_id, base_url):
    """
    make the message that send to slack
    """
    menu = Menu.objects.get(pk=menu_id)
    
    message = 'Hola!  Dejo el menú de hoy :)' + '\n'

    i = 1
    for option in menu.options.all():
        message+=str(i) + ') ' + option.name+'\n'
        i=i+1
    
    message+='Hagan su pedido en el link mas abajo. Tengan lindo día!' + '\n'
    message+='<' + base_url + 'menu/' + str(menu.uuid) + '|' + 'https://nora.cornershop.io/menu/' + str(menu.uuid) + '>'

    return message