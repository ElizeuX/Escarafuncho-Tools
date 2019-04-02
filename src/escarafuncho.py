
# escarafuncho :  Programa Python para análise Estenografica de arquivos
# sample program usage:  > python  escarafuncho.py -v -d c:\DIR_ORIGEM\ -r c:\DIR_RELATORIO\
#

'''
usage: Python file system escarafuncho... 

python escarafuncho [-h] [-v] -d ROOTPATH -r REPORTPATH

arguments:
  -h, --help          show this help message and exit
  -v, --verbose       allows progress messages to be displayed
  -d                  specify the root path for hashing
  -r                  specify the path where reports and logs will be written  
  e.g.                python  escarafuncho.py -v -d c:\DIR_ORIGEM\ -r c:\DIR_RELATORIO\
'''

import logging                    # Python Standard Library Logger
import time                       # Python Standard Library time functions
import sys                        # Python Standard Library system specific parameters
import _escarafuncho              # escarafuncho.py módulo que suporta as funções

if __name__ == '__main__':

    __VERSION__ = '0.1'
    __AUTHOR__ = Elizeu Ribeiro Sanches Xavier
    
    # Turn on Logging
    logging.basicConfig(filename='escarafunchador.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

    # Process the Command Line Arguments
    _escarafuncho.ParseCommandLine()

    # Record the Starting Time
    startTime = time.time()
    
    # Record the Welcome Message
    logging.info('')
    logging.info('Bemvindo ao Escarafunchador version 0.1 ... Novo scaneamento iniciado')
    logging.info('')
    _escarafuncho.DisplayMessage('Bemvindo ao Escarafunchador ... version '+ __VERSION__)

    # Record some information regarding the system
    logging.info('Sistema: '+ sys.platform)
    logging.info('Versão: '+ sys.version)
    
    # Traverse the file system directories and hash the files
    filesProcessed = _escarafuncho.WalkPath()

    # Record the end time and calculate the duration
    endTime = time.time()
    duration = endTime - startTime

    logging.info('Arquivos Processados: ' + str(filesProcessed) )
    logging.info('Tempo transcorrido: ' + str(duration) + ' segundos')
    logging.info('')
    logging.info('Programa Terminado Normalmente')
    logging.info('')

    _escarafuncho.DisplayMessage("Fim de execução")
    

