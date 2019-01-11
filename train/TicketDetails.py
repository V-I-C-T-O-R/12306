class TicketDetails(object):
    #  车次：3
    @property
    def trainNo(self):
        return self._trainNo

    @trainNo.setter
    def trainNo(self, trainNo):
        self._trainNo = trainNo

    @property
    def fromStation(self):
        return self._fromStation

    @fromStation.setter
    def fromStation(self, value):
        self._fromStation = value

    @property
    def toStation(self):
        return self._toStation

    @toStation.setter
    def toStation(self, value):
        self._toStation = value

    @property
    def startStation(self):
        return self._startStation

    @startStation.setter
    def startStation(self, value):
        self._startStation = value

    @property
    def endStation(self):
        return self._endStation

    @endStation.setter
    def endStation(self, value):
        self._endStation = value

    #  start_station_code:起始站：4
    @property
    def startStationCode(self):
        return self._startStationCode;

    @startStationCode.setter
    def startStationCode(self, value):
        self._startStationCode = value

    #  end_station_code终点站：5
    @property
    def endStationCode(self):
        return self._endStationCode

    @endStationCode.setter
    def endStationCode(self, value):
        self._endStationCode = value

    #  from_station_code:出发站：6
    @property
    def fromStationCode(self):
        return self._fromStationCode

    @fromStationCode.setter
    def fromStationCode(self, value):
        self._fromStationCode = value

    #  to_station_code:到达站：7
    @property
    def toStationCode(self):
        return self._toStationCode

    @toStationCode.setter
    def toStationCode(self, value):
        self._toStationCode = value

    #  start_time:出发时间：8
    @property
    def leaveTime(self):
        return self._leaveTime

    @leaveTime.setter
    def leaveTime(self, value):
        self._leaveTime = value

    #  arrive_time:达到时间：9
    @property
    def arriveTime(self):
        return self._arriveTime

    @arriveTime.setter
    def arriveTime(self, value):
        self._arriveTime = value

    #  历时：10
    @property
    def totalConsume(self):
        return self._totalConsume

    @totalConsume.setter
    def totalConsume(self, value):
        self._totalConsume = value

    #  商务特等座：32
    @property
    def businessSeat(self):
        return self._businessSeat

    @businessSeat.setter
    def businessSeat(self, value):
        self._businessSeat = value

    #  一等座：31
    @property
    def firstClassSeat(self):
        return self._firstClassSeat

    @firstClassSeat.setter
    def firstClassSeat(self, value):
        self._firstClassSeat = value

    #  二等座：30
    @property
    def secondClassSeat(self):
        return self._secondClassSeat

    @secondClassSeat.setter
    def secondClassSeat(self, value):
        self._secondClassSeat = value

    #  高级软卧：21
    @property
    def advancedSoftSleep(self):
        return self._advancedSoftSleep

    @advancedSoftSleep.setter
    def advancedSoftSleep(self, value):
        self._advancedSoftSleep = value

    #  软卧：23
    @property
    def softSleep(self):
        return self._softSleep

    @softSleep.setter
    def softSleep(self, value):
        self._softSleep = value

    #  动卧：33
    @property
    def moveSleep(self):
        return self._moveSleep

    @moveSleep.setter
    def moveSleep(self, value):
        self._moveSleep = value

    #  硬卧：28
    @property
    def hardSleep(self):
        return self._hardSleep

    @hardSleep.setter
    def hardSleep(self, value):
        self._hardSleep = value

    #  软座：24
    @property
    def softSeat(self):
        return self._softSeat

    @softSeat.setter
    def softSeat(self, value):
        self._softSeat = value

    #  硬座：29
    @property
    def hardSeat(self):
        return self._hardSeat

    @hardSeat.setter
    def hardSeat(self, value):
        self._hardSeat = value

    #  无座：26
    @property
    def noSeat(self):
        return self._noSeat

    @noSeat.setter
    def noSeat(self, value):
        self._noSeat = value

    #  其他：22
    @property
    def other(self):
        return self._other

    @other.setter
    def other(self, value):
        self._other = value

    #  备注：1
    @property
    def mark(self):
        return self._mark

    @mark.setter
    def mark(self, value):
        self._mark = value

        #
        #  start_train_date:车票出发日期：13

    @property
    def passengerType(self):
        return self._passengerType

    @passengerType.setter
    def passengerType(self, value):
        self._passengerType = value

    @property
    def secretStr(self):
        return self._secretStr

    @secretStr.setter
    def secretStr(self, value):
        self._secretStr = value

    @property
    def startDate(self):
        return self._startDate

    @startDate.setter
    def startDate(self, value):
        self._startDate = value

    def __str__(self):
        return '[车次:%s,出发站:%s,到达站:%s,出发时间:%s,到达时间:%s]' % (self._trainNo, self._fromStation,
                                                          self._toStation, self._leaveTime, self._arriveTime)

    __repr__ = __str__
