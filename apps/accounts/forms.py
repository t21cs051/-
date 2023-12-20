'''
Created on 2023/12/20

@author: t21cs019
'''

from django.contrib.auth.forms import AuthenticationForm 


class LoginForm(AuthenticationForm):
    """ログオンフォーム"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'text'
            field.widget.attrs['placeholder'] = field.label   
