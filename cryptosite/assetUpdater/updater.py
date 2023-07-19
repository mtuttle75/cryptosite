from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from assetUpdater import assetApi

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(assetApi.update_crypto_assets, 'interval', hours=24)
    scheduler.start()