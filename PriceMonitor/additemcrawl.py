# -*- coding: utf-8 -*-
import conn_sql


def additemcrawl(item_id, user_id, mall_id):
    query = conn_sql.ItemQuery()
    proxy = False
    try:
        item_name = query.crawl_name(item_id, proxy, mall_id)
    except:
        item_name = '首次抓取名称失败，等待重试'
    try:
        item_price = query.crawl_price(item_id, proxy, mall_id)
    except:
        item_price = '-1'
    # query.write_item_info(user_id, item_id, item_name, item_price)  # sqlite cursor报错
    # query.compare_send_email(user_id, item_id, item_price, item_name)
    return item_name, item_price
