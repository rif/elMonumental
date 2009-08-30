import socket
if socket.gethostname() in ('sro-9090.sro.oce.net', 'grace', 'love', 'newcreation'):
    from settings_development import *
else:
    from settings_production import *
