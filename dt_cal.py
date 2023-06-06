import datetime
from datetime import datetime
now =  datetime.now()
dd = now.strftime("%d")
mm = now.strftime("%m")
yy = now.strftime("%Y")
  
 

if len(dd) == 1:
    dd="0"+dd
    
if len(mm) == 1:
    mm="0"+mm
    
yy=yy[-2:]

path_name="/home/backup_"+dd+mm+yy+"_1.dump"
path_name="/Backup/backup_"+dd+mm+yy+"_1.dump"

print(path_name)

   
    
    