# -*- coding: utf-8 -*-


class HandleURL():
    except_key = []
    
    def handle_before_request(self, request):
        url = request.path
        print(url)
        if not url.endswith('/'):
            url += '/'
        request.path = url.replace('//', '/')