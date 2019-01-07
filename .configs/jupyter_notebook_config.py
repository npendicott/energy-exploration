# Set options for certfile, ip, password, and toggle off
# browser auto-opening
# c.NotebookApp.certfile = u'/absolute/path/to/your/certificate/mycert.pem'
# c.NotebookApp.keyfile = u'/absolute/path/to/your/certificate/mykey.key'

# Set ip to '*' to bind on all interfaces (ips) for the public server
# I think we need to use 0.0.0.0, not *
c.NotebookApp.ip = '0.0.0.0'

# TODO: What hash?
c.NotebookApp.password = u'sha1:2a5d557fde6f70baa63adc15bfb75516765afc8e'

c.NotebookApp.open_browser = False
# It is a good idea to set a known, fixed port for server access
c.NotebookApp.port = 8080
