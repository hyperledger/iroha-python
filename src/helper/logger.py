import logging

# ログの出力名を設定
logger = logging.getLogger(__name__)
# ログのコンソール出力の設定
sh = logging.StreamHandler()
logger.addHandler(sh)

# ログの出力形式の設定
formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
sh.setFormatter(formatter)

# ログレベルの設定
def setDebug():
    logger.setLevel(logging.DEBUG)

def setWarning():
    logger.setLevel(logging.WARNING)

def setInfo():
    logger.setLevel(logging.INFO)

def debug(message):
    logger.debug(message)

def warning(message):
    logger.warning(message)


def info(message):
    logger.info(message)