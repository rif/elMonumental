import socket
if socket.gethostname() in ('sro-1503.sro.oce.net', 'grace', 'love', 'newcreation', 'old-mac'):
    from settings_development import *
else:
    from settings_production import *
