def get_url_base(request):
    if request.is_secure():
        protocol = 'https://'
    else:
        protocol = 'http://'

    return protocol + request.META['HTTP_HOST'] + '/'