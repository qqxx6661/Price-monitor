# All time in seconds
ITEM_CRAWL_TIME = 600  # Monitor sleep time, if not using proxy, CRAWL_TIME > 1800 recommended.
CATE_CRAWL_TIME = 1800  # Category crawl sleep time, if not using proxy, CRAWL_TIME > 1800 recommended.
UPDATE_TIME = 100  # Find item updated before this time value
Email_TIME = 10  # Send email sleep time
PROXY_CRAWL = 0  # 1: Use proxy pool 0: Use local ip 2: zhi ma ip
THREAD_NUM = 1  # Crawler thread, 1 equals loop
THREAD_SLEEP_TIME = 5  # Sleep time for using LOCAL ip
PROXY_POOL_IP = "115.159.190.214"  # Your redis server ip
DISCOUNT_LIMIT = 0.8  # Set alert mail discount
