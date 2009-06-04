import socket
if socket.gethostname() == 'sro-9090.sro.oce.net':
    from settings_development import *
else:
    from settings_production import *

