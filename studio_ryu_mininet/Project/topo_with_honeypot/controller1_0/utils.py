class Utils():

    @staticmethod
    def host_to_port(host_ip):
        out_port = None
        if host_ip == '10.0.1.10':
           out_port = 1
        if host_ip == '10.0.1.11':
           out_port = 2
        if host_ip == '10.0.1.12':
           out_port = 3
        if host_ip == '10.0.1.13':
           out_port = 8
        if host_ip == '10.0.1.200':
           out_port = 7
        return out_port
              