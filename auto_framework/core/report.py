import requests
from core.logger import Logger

logger = Logger('report').getLogger()

# report_result = {}


def send_report(url, report):
    try:
        if url != "":
            res = requests.post(url, json=report)
            if res.status_code == 200:
                logger.debug("报告发送成功")
            else:
                logger.debug("报告发送失败,返回值{}".format(res.status_code))
        else:
            logger.debug("没有配置web端ip，未发送报告！")
    except Exception as e:
        logger.debug("报告发送失败{}".format(e))


