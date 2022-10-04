import time
import os
import json

# syslog = 'C:/Users/ironm/Desktop/putty.log'
# sleep_time_in_seconds = 1

# try:
#     with open(syslog, 'r', errors='ignore') as f:
#         while True:
#             for line in f:
#                 if line:
#                     print(line)
#                     # do whatever you want to do on the line
#             time.sleep(sleep_time_in_seconds)
# except IOError as e:
#     print('Cannot open the file {}. Error: {}'.format(syslog, e))

# if os.path.exists(syslog):
#     print("yes")
# with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Config.json"),'r',encoding="utf8") as f:
#     setup_dict = json.load(f)

# print(setup_dict["Others"]["WoDa"])
a = set()
a.add("ab")
a.add("cd")
print(a)
if "a" in ','.join(a):
    print("ya")
else:
    print("ne")
    
# print(','.join(a))
