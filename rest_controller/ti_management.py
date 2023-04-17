import topology as t
# THREAT INTELLIGENCE SUBNET MANAGEMENT

# indexes
COWRIE_INDEX = 0
HERALDING_INDEX = 1
SSH_INDEX = 0
TELNET_INDEX= 1
FTP_INDEX = 2
SOCKS5_INDEX = 3

# list of honeypots
honeypots = [t.cowrie, t.heralding1]

# list of services
services = ["ssh", "telnet", "ftp", "socks5"]

# service map (honeypots x services): rows = honeypot, columns = services supported
sm = [[1, 1, 0, 0], [1, 0, 1, 1]]

# service busy: sbn = 1 if it is busy, else it is 0
# default = all services are free
sb = [[0, 0, 0, 0], [0, 0, 0, 0]]
