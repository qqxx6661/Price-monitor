import datetime
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from CONFIG import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_CHARSET, EMAIL_FIRST_ALERT_WAIT_TIME, \
    DISCOUNT_LIMIT
from database.model.pm_mail_record import PmMailRecord
from database.model.pm_monitor_item import PmMonitorItem
from database.model.pm_user import PmUser


class SqlOperator:
    DBSession = None

    def __init__(self):
        """
        初始化数据库连接
        """
        conn = "mysql+pymysql://{}:{}@{}:{}/pm_backend?charset={}".format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST,
                                                                          MYSQL_PORT, MYSQL_CHARSET)
        logging.info("初始化数据库连接:{}".format(conn))
        engine = create_engine(conn)
        self.DBSession = sessionmaker(bind=engine)

    def update_pm_monitor_item(self, crawl_info, item_info, huihui_info):
        """
        更新商品数据
        """
        logging.info("更新京东商品数据开始：{} {}".format(crawl_info, item_info))
        if not item_info["price"]:
            logging.info("爬虫获取价格数据为空，不更新数据库")
            return
        session = self.DBSession()
        record = session.query(PmMonitorItem).filter(PmMonitorItem.id == crawl_info["id"]).one()
        # 已有价格数据，若价格变化，写入上次价格和折扣
        if record.price and float(record.price) != float(item_info["price"]):
            last_price = record.price
            discount = round(float(item_info["price"]) / float(last_price), 2)
            logging.info("商品价格变动，现价：{}，原价：{}，写入折扣：{}".format(item_info["price"], record.price, discount))
            record.discount = discount
            record.last_price = last_price
        record.name = item_info["name"]
        record.subtitle = item_info["subtitle"]
        record.price = item_info["price"]
        record.plus_price = item_info["plus_price"]
        record.max_price = huihui_info["max_price"]
        record.min_price = huihui_info["min_price"]
        record.gmt_modified = datetime.datetime.now()
        session.commit()
        session.close()
        logging.info("更新京东商品数据完成")

    def query_email_alert_needed(self, monitor_item_id):
        """
        查询是否需要邮件提醒：创建时间15分钟内不提醒
        """
        logging.info("查询表记录Id：{} 是否需要邮件提醒".format(monitor_item_id))

        # 取数据库
        session = self.DBSession()
        record = session.query(PmMonitorItem).filter(PmMonitorItem.id == monitor_item_id).one()
        user_price = record.user_price
        price = record.price
        plus_price = record.plus_price
        is_alert = record.is_alert
        gmt_create = record.gmt_create
        discount = record.discount
        # logging.info("user_price：{}".format(user_price))
        # logging.info("item_price：{}".format(price))
        # logging.info("plus_price：{}".format(plus_price))
        # logging.info("is_alert：{}".format(is_alert))
        # logging.info("gmt_create：{}".format(gmt_create))
        session.close()

        # 判断逻辑
        if not price:
            logging.info("爬虫获取价格数据为空，不提醒")
            return False
        lowest_price = user_price
        if plus_price:
            lowest_price = plus_price if (plus_price <= user_price) else user_price
        time_delta = datetime.datetime.now() - gmt_create
        # 商品价格低于设定价格
        if float(lowest_price) >= float(price) and is_alert == 1 and time_delta.total_seconds() > EMAIL_FIRST_ALERT_WAIT_TIME:
            return True
        # 商品价格有变化且低于折扣
        if discount and float(discount) <= DISCOUNT_LIMIT and is_alert == 1 and time_delta.total_seconds() > EMAIL_FIRST_ALERT_WAIT_TIME:
            return True
        return False

    def query_pm_monitor_item(self, monitor_item_id):
        """
        查询pm_monitor_item表
        """
        session = self.DBSession()
        record = session.query(PmMonitorItem).filter(PmMonitorItem.id == monitor_item_id).one()
        session.close()
        return record


    def query_user_info(self, monitor_item_id):
        """
        通过监控表Id查询用户Id，然后查用户表获取信息
        """
        logging.info("查用户表获取信息：{}".format(monitor_item_id))

        # 查询pm_monitor_item表
        session = self.DBSession()
        record_pm_monitor_item = session.query(PmMonitorItem).filter(PmMonitorItem.id == monitor_item_id).one()
        user_id = record_pm_monitor_item.user_id
        logging.info("user_id：{}".format(user_id))

        # 查询pm_user表
        record_pm_user = session.query(PmUser).filter(PmUser.id == user_id).one()
        name = record_pm_user.name
        email = record_pm_user.email
        session.close()

        logging.info("name：{}".format(name))
        logging.info("email：{}".format(email))
        user_info = {"name": name, "email": email}
        return user_info

    def update_alert_info(self, monitor_item_id, status):
        """
        修改监控表is_alert状态值
        """
        logging.info("更新监控表is_alert状态值开始：{} {}".format(monitor_item_id, status))
        session = self.DBSession()
        record = session.query(PmMonitorItem).filter(PmMonitorItem.id == monitor_item_id).one()
        record.is_alert = status
        session.commit()
        session.close()
        logging.info("更新监控表is_alert状态值完成")

    def insert_pm_mail_record(self, address, sender, receiver, subject, text, is_sent):
        """
        发送邮件记录
        """
        logging.info("插入邮件记录pm_mail_record：{} {} {} {} {} {}".format(address, sender, receiver, subject, text, is_sent))
        session = self.DBSession()
        record = PmMailRecord(address=address, _from=sender, to=receiver, subject=subject, content=text, is_sent=is_sent,
                              gmt_create=datetime.datetime.now(), gmt_modified=datetime.datetime.now())
        session.add(record)
        session.commit()
        session.close()


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s %(filename)s %(funcName)s %(lineno)s %(levelname)s - %("
                               "message)s", datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.INFO)
    sqlOperator = SqlOperator()

    # sqlOperator.update_pm_monitor_item({'id': "582", 'item_id': "8738639"},
    #                                    {'name': '五月花(May Flower) 抽纸 婴儿柔特级柔厚4层90抽面巾纸*6包（小规格）', 'price': '14.90',
    #                                     'plus_price': None, 'subtitle': '生活就是这样，越努力，越幸运五月花，婴儿柔为优秀的你而生！(此商品不参加上述活动)'}
    #                                    , {'max_price': 34.9, 'min_price': 34.2})

    logging.info(sqlOperator.query_email_alert_needed(1509))

    # logging.info(sqlOperator.query_user_info(582))

    # logging.info(sqlOperator.query_pm_monitor_item(582).__dict__)