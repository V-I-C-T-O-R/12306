
ips = []

def init_ip_pool():
    import os

    from utils.sqllite_handle import Sqlite
    address = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/'
    sqlite = Sqlite(address + 'ip.db')
    ips_results = sqlite.query_data('select proxy_adress from ip_house')
    for ip in ips_results:
        ips.append(ip[0])

init_ip_pool()