"""A basic (single function) API written using Hug"""
import hug


#@hug.get('/happy_birthday', examples="name=HUG&age=1")
#def happy_birthday(name: hug.types.text, age: hug.types.number):
#    """Says happy birthday to a user"""
#    return "Happy {0} Birthday {1}!".format(name, age)


import hug
#import requests


@hug.cli()
@hug.local()
@hug.get()
#def top_post(section: hug.types.one_of(('news', 'newest', 'show'))): #='news'):
def top_post(section: hug.types.one_of(('news', 'newest', 'show'))='news'):
    """Returns the top post from the provided section"""
    #content = requests.get('https://news.ycombinator.com/{0}'.format(section)).content
    #text = content.decode('utf-8')
    #return text.split('<tr class=\'athing\'>')[1].split("<a href")[1].split(">")[1].split("<")[0]
    return f'section: {section}'


@hug.cli(output_format=hug.output_format.json)
@hug.get(output=hug.output_format.html)
@hug.local()
def happy_birthday(name: hug.types.text, age: hug.types.number=3):#, hug_timer=3):
    """2nd birthday"""
    return {'messsage': f'Happy {age} Birthday {name}',
            #'took': float(hug_timer)}
            }


#from hug_test_sub import home, sub, index
import hug_test_sub

print(dir(hug_test_sub))
print(hug_test_sub._http)
hug.API(__name__).extend(hug_test_sub, '/sub')

#hug.get('/home', api=hug.API(__name__))(home)
#
##hug.http(prefixes='/sub', api=hug.API(__name__))(index)
#print(sub.api, sub.api.name)
#sub.api = hug.API(__name__)
#print(sub.api, sub.api.name)
#print(hug.API(__name__), hug.API(__name__))


r"""
>>> api = hug.API(__name__)
>>> print(type(api))
<class 'hug.api.API'>
>>> router = hug.route.API(__name__)
>>> print(type(router))
<class 'hug.route.API'>
>>> print(type(router.get()))
<class 'hug.routing.URLRouter'>
>>> api = hug.get('/home', api=hug.API(__name__))
>>> print(type(api))
<class 'hug.routing.URLRouter'>
>>> api = hug.get(on_invalida=hug.redirect.not_found)
>>> print(type(api))
<class 'hug.routing.URLRouter'>
"""


if __name__ == '__main__':
    #top_post.interface.cli()
    help(hug.get)
