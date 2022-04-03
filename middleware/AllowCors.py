# -*- coding: utf-8 -*-


class AllowCors():
    
    def handle_after_request(self, environ):
        environ.headers['Access-Control-Allow-Origin'] = '*'
        return environ