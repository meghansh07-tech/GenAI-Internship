import schedule
import time

from utils.updater import update_knowledge_base


def run_update():

    print("Checking for new documents...")

    update_knowledge_base()



# Run update every 24 hours
schedule.every(24).hours.do(run_update)


print("Knowledge base scheduler started...")


while True:

    schedule.run_pending()

    time.sleep(60)