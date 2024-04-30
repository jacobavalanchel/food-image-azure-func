# DateTimeSettings
import os

class FlaskConfig:
    """开发环境"""
    DEBUG = True
    # .....
    APP_SECRET_KEY =  b'_5#y2L"F4Q8z\n\xec]/'
    # jwt 相关配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-xxx'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_CHECK_FORM = True
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') or 3600
    PROPAGATE_EXCEPTIONS = True