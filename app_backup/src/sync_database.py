from tasks import sync_databases
from databases import databases_urls
import time

def sync_database():
    while True:
        time.sleep(20)
        for database_url in databases_urls:
            sync_databases(database_url)

if __name__ == "__main__":
    sync_database()
