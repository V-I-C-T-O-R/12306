class PassengerDetails(object):
    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def passengerName(self):
        return self._passengerName

    @passengerName.setter
    def passengerName(self, value):
        self._passengerName = value

    @property
    def sexCode(self):
        return self._sexCode

    @sexCode.setter
    def sexCode(self, value):
        self._sexCode = value

    @property
    def sexName(self):
        return self._sexName

    @sexName.setter
    def sexName(self, value):
        self._sexName = value

    @property
    def bornDate(self):
        return self._bornDate

    @bornDate.setter
    def bornDate(self, value):
        self._bornDate = value

    @property
    def countryCode(self):
        return self._countryCode

    @countryCode.setter
    def countryCode(self, value):
        self._countryCode = value

    @property
    def passengerIdTypeCode(self):
        return self._passengerIdTypeCode

    @passengerIdTypeCode.setter
    def passengerIdTypeCode(self, value):
        self._passengerIdTypeCode = value

    @property
    def passengerIdTypeName(self):
        return self._passengerIdTypeName

    @passengerIdTypeName.setter
    def passengerIdTypeName(self, value):
        self._passengerIdTypeName = value

    @property
    def passengerIdNo(self):
        return self._passengerIdNo

    @passengerIdNo.setter
    def passengerIdNo(self, value):
        self._passengerIdNo = value

    @property
    def passengerType(self):
        return self._passengerType

    @passengerType.setter
    def passengerType(self, value):
        self._passengerType = value

    @property
    def passengerFlag(self):
        return self._passengerFlag

    @passengerFlag.setter
    def passengerFlag(self, value):
        self._passengerFlag = value

    @property
    def passengerTypeName(self):
        return self._passengerTypeName

    @passengerTypeName.setter
    def passengerTypeName(self, value):
        self._passengerTypeName = value

    @property
    def mobileNo(self):
        return self._mobileNo

    @mobileNo.setter
    def mobileNo(self, value):
        self._mobileNo = value

    @property
    def phoneNo(self):
        return self._phoneNo

    @phoneNo.setter
    def phoneNo(self, value):
        self._phoneNo = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def postalcode(self):
        return self._postalcode

    @postalcode.setter
    def postalcode(self, value):
        self._postalcode = value

    @property
    def firstLetter(self):
        return self._firstLetter

    @firstLetter.setter
    def firstLetter(self, value):
        self._firstLetter = value

    @property
    def recordCount(self):
        return self._recordCount

    @recordCount.setter
    def recordCount(self, value):
        self._recordCount = value

    @property
    def totalTimes(self):
        return self._totalTimes

    @totalTimes.setter
    def totalTimes(self, value):
        self._totalTimes = value

    @property
    def indexId(self):
        return self._indexId

    @indexId.setter
    def indexId(self, value):
        self._indexId = value

    def __str__(self):
        return '[name: %s,' \
               'sex: %s' \
               'birth: %s' \
               'id: %s' \
               'phone: %s' \
               'email: %s' \
               'passengerType: %s]' % (self._passengerName or '',
                                       self._sexName or '',
                                       self._bornDate or '',
                                       self._passengerIdNo or '',
                                       self._mobileNo or '',
                                       self._email or '',
                                       self._passengerType or '')

    __repr__ = __str__
