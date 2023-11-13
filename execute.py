import os
import time
from qgis.core import *
import dotenv
dotenv.load_dotenv()

# init qgis
QgsApplication.setPrefixPath(os.getenv('QGIS_PREFIX_PATH'), True)
qgs = QgsApplication([], True)
qgs.initQgis()

# loading main code
import os
import sys
modules_path = os.getcwd()
if sys.platform == 'win32':
    modules_path = modules_path.replace('\\', '\\\\')

sys.path.append(modules_path+'/functions')
print('loaded modules from: ', modules_path)

from main import main
print('-----------------------------------------')
print('            starting execution')
print('-----------------------------------------')
time_start = time.time()
main()
time_end = time.time()
execution_time = time_end - time_start
print('-----------------------------------------')
print('execution time: ', execution_time, '[s]')
print('-----------------------------------------')

# closgin qgis
qgs.exitQgis()