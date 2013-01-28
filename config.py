# XBMC Connection details
XBMCIP = "192.168.178.52"
XBMCTCPPORT = "9090"
XBMCHTTPPORT = "8081"
XBMCUSER = "xbmc"
XBMCPASS = "xbmc"


# Update config in seconds
AUTOSETSLIDERINT = 0.1
AUTOUPDATESLIDER = 2

#do not edit this
XBMCHTTPRPCURL = ''.join(["http://", XBMCUSER, ":", XBMCPASS, "@", XBMCIP, ":", XBMCHTTPPORT, "/jsonrpc"])