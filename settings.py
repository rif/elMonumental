import socket
if socket.gethostname() in ('sro-1503.sro.oce.net', 'grace', 'love', 'newcreation', 'Old-Mac.local'):
    from settings_development import *
else:
    from settings_production import *
