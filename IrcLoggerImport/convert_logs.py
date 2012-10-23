import os
import json
import time
WEEK_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

all_files = os.listdir(".")
all_files_sorted = sorted(all_files, reverse=True)

for filename in all_files_sorted:
   if filename.endswith(".json"):
      print 'opening file %s' % filename
      f = open(filename, 'r')
      txt = f.read()
      js = json.loads(txt)
      f.close()
      channel_name = filename.split('.')[0]
      print 'exporting channel %s' % channel_name	  
      if not os.path.exists(channel_name):
         os.mkdir(channel_name)
      for item in js:
         msg = unicode(item['message'])
         user = item['user']['username']
         msg_date = item['date_created']
         msg_date_struct = time.localtime(msg_date)
         #related_file_name = '%s/%s-%s-%s,%s.log' % (channel_name, msg_date_struct.tm_year, msg_date_struct.tm_mon, msg_date_struct.tm_mday, WEEK_DAYS[msg_date_struct.tm_wday])
         related_file_name = '%s/%s-%02d-%02d,%s.log' % (channel_name, msg_date_struct.tm_year, msg_date_struct.tm_mon, msg_date_struct.tm_mday, WEEK_DAYS[msg_date_struct.tm_wday])
         if msg.find('ACTION is away') == -1 and msg.find('ACTION is back') == -1:
            out = open(related_file_name, 'a')
            #out.write('User: %s,   Message: %s\r\n' % (related_file_name, user, msg.encode('utf-8')))
            out.write('[%02d:%02d] <%s> %s\n' % (msg_date_struct.tm_hour, msg_date_struct.tm_min, user, msg.encode('utf-8')))
            out.close()