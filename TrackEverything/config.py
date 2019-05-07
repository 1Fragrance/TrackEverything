

# Common config
class Config(object):
    pass


# Dev config
class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_HOST = 'mongodb://localhost:27017/local'


# Prod config
class ProductionConfig(Config):
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
