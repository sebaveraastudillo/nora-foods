from nora.celery import app
from .models import Menu
import requests

@app.task
def send_menu(base_url, menu_id):
    menu = Menu.objects.get(pk=menu_id)
    
    message = 'Hola!  Dejo el menú de hoy :)' + '\n'

    i = 1
    for option in menu.options.all():
        message+=str(i) + ') ' + option.name+'\n'
        i=i+1
    
    message+='Hagan su pedido en el link mas abajo. Tengan lindo día!' + '\n'
    message+='<' + base_url + 'menu/' + str(menu.uuid) + '|' + 'https://nora.cornershop.io/menu/' + str(menu.uuid) + '>'

    r = requests.post('https://slack.com/api/chat.postMessage', params={
        "token": "xoxp-728764217476-729226154192-729227634720-738190b28f7a40c36bceb9ddc736ccec",
        "channel": "CMF6X85TP",
        "text": message
    }) 