'''
Created on 2024/01/01

@author: t21cs019
Access restrictions
'''

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect

class authMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path != '/accounts/login/' and not request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login/')
        return response
