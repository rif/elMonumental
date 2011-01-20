import socket
if socket.gethostname() in ('sro-1503.sro.oce.net', 'grace', 'love', 'newcreation', 'old-mac', 'Virgils-Mac-Pro-4.local'):
    from settings_development import *
else:
    from settings_production import *
