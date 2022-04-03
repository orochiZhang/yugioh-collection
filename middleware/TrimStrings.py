# -*- coding: utf-8 -*-

class TrimStrings(object):
    except_key = []
    
    def handle_before_request(self, request):
        print('TrimStrings', request.args)
    