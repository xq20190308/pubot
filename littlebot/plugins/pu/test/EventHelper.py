import time
from datetime import datetime

event_regStartTime = datetime.fromtimestamp(time.time())  # 转换为 datetime 对象
print(event_regStartTime.strftime("%Y-%m-%d %H:%M:%S"))