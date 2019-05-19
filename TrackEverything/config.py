# Common config
class Config(object):
    DEBUG = True
    LOG_FILENAME = 'log.txt'


# Dev config
class DevelopmentConfig(Config):
    MONGODB_HOST = 'mongodb://localhost:27017/local'


# Prod config
class ProductionConfig(Config):
    DEBUG = False


class TestConfig(Config):
    TESTING = True
    MONGODB_HOST = 'mongodb://localhost:27017/test'


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig
}
