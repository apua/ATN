_v = lambda name, i=__import__('inspect'): print(f'DEBUG value: {name} -> %s' %
        (lambda f=i.getouterframes(i.currentframe())[1].frame: f.f_locals[name] if name in f.f_locals else f.f_globals[name])()
        )
_t = lambda name, i=__import__('inspect'): print(f'DEBUG type: {name} -> %s' %
        (lambda f=i.getouterframes(i.currentframe())[1].frame: f.f_locals[name] if name in f.f_locals else f.f_globals[name])()
        )

