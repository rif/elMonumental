import socket
if socket.get_hostname() == 'sro-9090.sro.oce.net':
    from settings_development import *
else:
    from settings_production import *

