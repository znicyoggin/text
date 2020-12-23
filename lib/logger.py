import time
from datetime import date
import logging
import logging.handlers

#Log Writing functions

def initialize_logger(file_name, logger_level):
	#today_str = (date.today()).isoformat()
	#file_name = file_name + "." + today_str + ".log"
	logger = logging.getLogger(file_name)
	logger.setLevel(logger_level)
	handler = logging.handlers.TimedRotatingFileHandler(  	file_name, 
															when='W0', 
															interval=1, 
															backupCount=8, )
															
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.debug("Starting log file for script execution.")
	return logger