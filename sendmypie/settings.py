import logging
import logging.config
import sys


logging.basicConfig(level=logging.INFO)
logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s-%(name)6s - %(levelname)6s - %(filename)6s-ligne: %(lineno)5d - %(funcName)s - \t%(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level':'DEBUG',
            'stream': sys.stdout,
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'level':'DEBUG',
            'filename': './log/logs_sendmypie.log',
            'maxBytes': 700000000,
            'backupCount': 20
        }
    },
    'loggers': {
        'sendmypie.main': {
            'handlers': ['file'],
            'propagate': False,
        },
        'sendmypie.tests': {
            'handlers': ['file'],
            'propagate': False,
        }
    }
}

def dictConfig(logging_config):
    logging.config.dictConfigClass(logging_config).configure()

dictConfig(logging_config)