from django.forms import ModelForm
from automated_test.models import *

class A(ModelForm):
    class Meta:
        model = ExecLayer
        #fields = ['id', 'ip']
        exclude = []

A = type('', (ModelForm,), {'Meta': type('',(),{'model': ExecLayer, 'exclude': ()})})


assert A({'id':1, 'ip':'1.1.1.1'}).is_valid()
assert not A({'id':1, 'ip':'1.1.1'}).is_valid()
assert not A({'id':1}).is_valid()
assert A({'ip':'1.1.1.1'}).is_valid()
