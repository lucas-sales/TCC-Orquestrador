import time
import schedule

from src.services.handler import Handler

if __name__ == "__main__":
    # schedule.every(int(1)).minutes.do(Handler().run)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    Handler().run()
