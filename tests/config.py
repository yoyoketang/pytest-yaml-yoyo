
class Config:
    version = "v1.0"


class TestConfig(Config):
    """测试环境"""
    BASE_URL = 'http://124.70.221.221:8201'
    MYSQL_HOST = "124.70.221.221"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "yoyo123456"
    MYSQL_PORT = 3309
    MYSQL_DATABASE = "apps"


class UatConfig(Config):
    """联调环境"""
    BASE_URL = 'http://124.70.221.221:8201'
    MYSQL_HOST = "124.70.221.221"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "yoyo123456"
    MYSQL_PORT = 3309
    MYSQL_DATABASE = "apps"


# 环境关系映射，方便切换多环境配置
env = {
    "test": TestConfig,
    "uat": UatConfig
}
