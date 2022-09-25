import time
import os

syslog = 'C:/Users/ironm/Desktop/putty.log'
sleep_time_in_seconds = 1

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

if os.path.exists(syslog):
    print("yes")
