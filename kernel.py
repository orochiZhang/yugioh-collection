# -*- coding: UTF-8 -*-
from flask import request
from middleware.HandleURL import HandleURL
from middleware.TrimStrings import TrimStrings
from middleware.AllowCors import AllowCors

class Kernel():
    # The application's global HTTP middleware stack.
    # These middleware are run during every request to your application.
    before_middleware = [
        TrimStrings(),
        HandleURL(),
    ]
    
    after_middleware = [
        AllowCors()
    ]
    
    def before_request(self):
        for obj in self.before_middleware:
            obj.handle_before_request(request)
    
    def after_request(self, environ):
        for obj in self.after_middleware:
            environ = obj.handle_after_request(environ)
        return environ