from datetime import datetime

created_at = 'Mon Jun 8 10:51:32 +0000 2009'
dt = datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')

print dt
