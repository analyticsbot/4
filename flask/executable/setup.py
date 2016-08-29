from distutils.core import setup
import py2exe
import sys
import numpy
import zmq, os
sys.setrecursionlimit(5000)
import matplotlib

#os.environ["PATH"] = os.environ["PATH"] + os.path.pathsep + os.path.split(zmq.__file__)[0]
##setup(console=['rest_api_v8.py'],
##      options = {
##          'py2exe':{
##              'packages':['pandas','flask','sklearn',\
##                          'numpy', 'dateutil', 'itertools'\
##                          ]
##              }
##          }
##      )
os.environ["PATH"] = os.environ["PATH"] + '; C:\\Python27\\DLLs'
setup(console=['rest_api_v8.py'],
    options={
           'py2exe': {'includes': ['pandas','flask','sklearn',\
                          'numpy', 'dateutil', 'itertools',"zmq.utils",\
                                   "zmq.utils.jsonapi", "zmq.utils.strtypes"],
                      "dll_excludes": ["MSVCP90.dll", 'pywintypes27.dll'],\
                      'excludes': ['_gtkagg', '_tkagg'],}
           }
    )
