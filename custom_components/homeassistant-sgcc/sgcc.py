import requests
import logging
import datetime

_LOGGER = logging.getLogger(__name__)

DETAIL_URL = "http://zdpay.ztendata.com/wx/zs/dayBillDetails?data="
ROOMINFO_URL = "http://zdpay.ztendata.com/wx/zs/getUserBindingRoomInfo?data="
BILL_URL = "http://zdpay.ztendata.com/wx/zs/billAndRecharge?data="
UPDATE_URL = "http://zdpay.ztendata.com/wx/zs/realTime/getTheMargin?data="

class SGCCData:
    def __init__(self, certificate, userid):
        self.userid = userid
        self._info = {}
        self.headers = {
            "Host": "zdpay.ztendata.com",
            "Referer" : "http://zdpay.ztendata.com/wx/zs/index",
            "Origin" : "http://zdpay.ztendata.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Cookie": f"CERTIFICATE={certificate}",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 "
                          "(KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x1800072c) "
                          "NetType/WIFI Language/zh_CN",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Accept": "*/*",
        }

    def update(self):
        url = UPDATE_URL+ "{roomTag: '" + str(self.roomtag) + "'}"
        ret = True
        try:
            r = requests.post(url, headers=self.headers, timeout=10)
            if r.status_code == 200:
                _LOGGER.debug(f"get UPDATE: {r.text}")
                result = r.json()
                if result["code"] == 0:
                    self._info["allowance"] = result["data"]
                else:
                    ret = False
                    _LOGGER.error(f"get UPDATE:{result['msg']}")
            else:
                ret = False
                _LOGGER.error(f"get UPDATE status_code = {r.status_code}")
        except Exception as e:
            ret = False
            _LOGGER.error(f"get UPDATE got error: {e}")
        return ret

    def getRoomInfo(self):
        url = ROOMINFO_URL+ "{userId: '" + str(self.userid) + "'}"
        ret = True
        try:
            r = requests.post(url, headers=self.headers, timeout=10)
            if r.status_code == 200:
                _LOGGER.debug(f"get RoomInfo: {r.text}")
                result = r.json()
                if result["code"] == 0:
                    self.roomtag = result["data"][0]["roomTag"]
                    self._info["roomid"] = result["data"][0]["roomId"]
                    self._info["address"] = result["data"][0]["address"]
                    self._info["allowance"] = result["data"][0]["allowance"]
                    self._info["price"] = result["data"][0]["djPrice"]
                else:
                    ret = False
                    _LOGGER.error(f"get RoomInfo:{result['msg']}")
            else:
                ret = False
                _LOGGER.error(f"get RoomInfo status_code = {r.status_code}")
        except Exception as e:
            ret = False
            _LOGGER.error(f"get RoomInfo got error: {e}")
        return ret
    
    def getBill(self):
        url = BILL_URL+ "{userId: '" + str(self.userid) + "',+roomTag: '" + str(self.roomtag) + "'}"
        ret = True
        try:
            r = requests.post(url, headers=self.headers, timeout=10)
            if r.status_code == 200:
                _LOGGER.debug(f"get Bill: {r.text}")
                result = r.json()
                if result["code"] == 0:
                    self._info["month_elec"] = result["data"][0]["electric"]
                    self._info["month_bill"] = result["data"][0]["money"]
                    self._info["bill"] = result["data"]
                    self._info["recharge"] = result["affix"]
                else:
                    ret = False
                    _LOGGER.error(f"get Bill:{result['msg']}")
            else:
                ret = False
                _LOGGER.error(f"get Bill status_code = {r.status_code}")
        except Exception as e:
            ret = False
            _LOGGER.error(f"get Bill got error: {e}")
        return ret
    
    def getDetail(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        url = DETAIL_URL+ "{roomTag: '" + str(self.roomtag) + "', year: '" + str(year) + "', month: '" + str(month) + "'}"
        ret = True
        try:
            r = requests.post(url, headers=self.headers, timeout=10)
            if r.status_code == 200:
                _LOGGER.debug(f"get Detail: {r.text}")
                result = r.json()
                if result["code"] == 0:
                    self._info["detail"] = result["data"]
                else:
                    ret = False
                    _LOGGER.error(f"get Detail:{result['msg']}")
            else:
                ret = False
                _LOGGER.error(f"get Detail status_code = {r.status_code}")
        except Exception as e:
            ret = False
            _LOGGER.error(f"get Detail got error: {e}")
        return ret

    def getData(self):
        if self.getRoomInfo():
            self.update()
            self.getBill()
            self.getDetail()
        _LOGGER.debug(f"Data {self._info}")
        return self._info
