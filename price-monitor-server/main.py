# -*- coding: utf-8 -*-
from conn_sql import ItemQuery

# config
break_time = 20  # set waiting time for one crawl round

itemquery = ItemQuery()
itemquery.start_monitor(break_time)
