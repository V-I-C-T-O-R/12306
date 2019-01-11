from fuckeverything import working

def setArgs():
    from optparse import OptionParser

    usage = "usage: python 12306.py [options] arg1 [options] arg2 ..."
    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--username", dest="username", default=None, type=str,
                      help="username/用户名，默认None")
    parser.add_option("-p", "--password", dest="password", default=None, type=str,
                      help="password/密码，默认None")
    parser.add_option("-f", "--from_station", dest="from_station", default=None, type=str,
                      help="from station/起始站，默认None")
    parser.add_option("-t", "--to_station", dest="to_station", default=None, type=str,
                      help="to station/终点站，默认None")
    parser.add_option("-d", "--day", dest="day", default=None, type=str,
                      help="day/日期，默认None")
    parser.add_option("-i", "--ids", dest="ids", default=None, type=str,
                      help="id cards,split by ','/身份证id,通过','分隔，默认None")
    parser.add_option("-e", "--type", dest="type", default='dc', type=str,
                      help="bill type,dc,wc/单程或双程，默认dc")
    parser.add_option("-l", "--policy", dest="policy", default=1, type=int,
                      help="bill policy/下单策略，1：全部提交，2：部分提交.，默认1")
    parser.add_option("-n", "--trains", dest="trains", default='', type=str,
                      help="train no/指定列车编号，默认''")
    parser.add_option("-s", "--seat", dest="seat", default='1', type=str,
                      help="custom seat/指定座位，默认'1',座位列表：商务座(9),特等座(P),一等座(M),二等座(O),高级软卧(6),软卧(4),硬卧(3),软座(2),硬座(1),无座(1)")
    parser.add_option("-r", "--refersh", dest="refersh", default=3, type=int,
                      help="refersh time/刷新时间，默认3s")
    return parser.parse_args()

def run():
    options, args = setArgs()
    username = options.username
    password = options.password
    day = options.day
    from_station = options.from_station
    to_station = options.to_station
    ids = options.ids
    tour_type = options.type
    policy = options.policy
    trains = options.trains
    seats = options.seat
    refersh = options.refersh
    if not username or not password or not day or not from_station or not to_station:
        return '必填信息不能为空:username,password,day,fromStation,toStation'
    ids = ids.split(',')
    tour_type = tour_type.split(',')
    trains = trains.split(',')
    seats = seats.split(',')
    working(username=username,password=password,id_cards=ids,day=day,from_station=from_station,
            to_station=to_station,seats=seats,types=1,train_no=trains,polocy=policy,tour_flag=tour_type,refersh=refersh)


if __name__ == '__main__':
    run()

