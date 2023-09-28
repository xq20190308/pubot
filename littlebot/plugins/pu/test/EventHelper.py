from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime
# 创建后台调度器
scheduler = BackgroundScheduler()

# 定义任务函数
def job():
    print("定时任务执行：", time.strftime("%Y-%m-%d %H:%M:%S"))
    # 添加定时任务，每隔5秒执行一次
scheduler.add_job(job, 'date', next_run_time=datetime.fromtimestamp(1695889620))

# 启动调度器
scheduler.start()

# 主线程等待一段时间后结束
time.sleep(20)

# 关闭调度器
scheduler.shutdown()

print("主线程结束")