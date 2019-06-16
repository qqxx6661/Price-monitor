# All time in seconds
ITEM_CRAWL_TIME = 600  # Monitor sleep time, if not using proxy, CRAWL_TIME > 1800 recommended.
UPDATE_TIME = 100  # Crawl item which updated before this time value
Email_TIME = 10  # Send email sleep time
PROXY_CRAWL = 0  # 1: Use proxy pool 0: Use local ip 2: Use zhi ma ip
PROXY_POOL_IP = "127.0.0.1"  # Your redis server ip
DISCOUNT_LIMIT = 0.8  # Set alert mail discount
