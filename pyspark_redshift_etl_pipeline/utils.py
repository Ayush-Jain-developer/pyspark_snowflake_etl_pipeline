import logging

logging.basicConfig(filename="app.log",
                    level=logging.INFO,
                    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')

