import logging
from django.core.management import call_command

# Get a logger instance
logger = logging.getLogger('django')

# Trigger an error log
logger.error('This is a test error message')

# Or for critical log
logger.critical('This is a test critical message')