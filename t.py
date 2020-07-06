import re

x = re.findall("课时(\d+)", "课时1223")

print(x)

"""
dkzp6zxxh
dkzp6zxxh

djh38aydh
"""

s = {"result": 0,
     "msg": "查询",
     "data": [
         {"appId": "djh38aydh", "hubName": "cloudclass", "kickUser": 0, "maxUsers": 5, "outputFps": 15,
          "outputKbps": 1500,
          "rtcHeight": 576, "rtcWidth": 886, "title": "pc_1920x1080(1600x1040)"},
         {"appId": "dkzouyurh", "hubName": "cloudclass", "kickUser": 0, "maxUsers": 10, "outputFps": 15,
          "outputKbps": 1500,
          "rtcHeight": 728, "rtcWidth": 1046, "title": "pc_1366x768(1046x728)"},
         {"appId": "dkzox6x4t", "hubName": "cloudclass", "kickUser": 0, "maxUsers": 10, "outputFps": 15,
          "outputKbps": 1500,
          "rtcHeight": 825, "rtcWidth": 1075, "title": "pc_1440x900(1120x860)"},
         {"appId": "dkzp2sysi", "hubName": "cloudclass", "kickUser": 0, "maxUsers": 10, "outputFps": 15,
          "outputKbps": 1500,
          "rtcHeight": 720, "rtcWidth": 1070, "title": "pc_1600x900(1280x860)"},
         {"appId": "dkzp6zxxh", "hubName": "cloudclass", "kickUser": 0, "maxUsers": 10, "outputFps": 15,
          "outputKbps": 1500,
          "rtcHeight": 720, "rtcWidth": 1280, "title": "8橙云课 手机 通用"},
         {"appId": "dl05u8bi5", "hubName": "cloudclass", "kickUser": 0, "maxUsers": 10, "outputFps": 15,
          "outputKbps": 1500,
          "rtcHeight": 590, "rtcWidth": 1280, "title": "iphonex"},
         {"appId": "dl05whkbm", "hubName": "cloudclass", "kickUser": 0, "maxUsers": 10, "outputFps": 15,
          "outputKbps": 1000,
          "rtcHeight": 720, "rtcWidth": 1080, "title": "mzvideo"},
         {"appId": "dl2b1o5dp", "hubName": "cloudclass", "kickUser": 0, "maxUsers": 10, "outputFps": 15,
          "outputKbps": 1000,
          "rtcHeight": 540, "rtcWidth": 960, "title": "云课web版"},
         {"appId": "dl2b61gzh", "hubName": "cloudclass", "kickUser": 0, "maxUsers": 10, "outputFps": 15,
          "outputKbps": 1500,
          "rtcHeight": 720, "rtcWidth": 960, "title": "pc1280-320"},
         {"appId": "dl2ppuuxu", "hubName": "cloudclass", "kickUser": 0, "maxUsers": 10, "outputFps": 15,
          "outputKbps": 2000,
          "rtcHeight": 768, "rtcWidth": 1024, "title": "8橙云课 ipad"}]
     }

asdasd = {"code": 0, "data": {"voteList": [
    {"classroomId": "69ccc40adf9446c7b7a997e93c25dbec", "craeteUserId": 4474641041984512,
     "createTime": "2020-07-06 16:22:41", "duration": 10, "multiSelect": 2, "optionValues": "",
     "startVoteTime": 1594023760673, "status": 0, "userChoose": "", "voteContent": "56", "voteEnd": 0,
     "voteEndTime": "", "voteId": "2da23a3544a640778c5de95a990e53b8", "voteKey": "1", "voteNumber": 0,
     "voteOptionList": []}], "systemTime": 1594023766502}, "msg": "成功", "result": 0}

fasfa = {"code": 0, "data": {"voteList": [
    {"classroomId": "6ed6133e013d4a58b129b022e0985ba5", "craeteUserId": 4474641041984512,
     "createTime": "2020-07-06 16:20:09", "duration": 10, "multiSelect": 2, "optionValues": "来看看",
     "startVoteTime": 1594023608998, "status": 0, "userChoose": "", "voteContent": "123", "voteEnd": 0,
     "voteEndTime": "", "voteId": "48a032083d7a4c18ac3eb1ce34df108a", "voteKey": "1", "voteNumber": 1,
     "voteOptionList": []}], "systemTime": 1594023685968}, "msg": "成功", "result": 0}
