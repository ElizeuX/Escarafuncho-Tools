'''
 Copyright (c) 2019 Elizeu Ribeiro Sanches Xavier

 Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
 documentation files (the "Software"), to deal in the Software without restriction, including without 
 limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of 
 the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all copies or 
 substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
 TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
 THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
 CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
 DEALINGS IN THE SOFTWARE.
'''

# escarafunchador : Extração de arquivos escondidos em imagens
# sample program usage:  > python Escarafuncho.py -v --sha256 -d E:/ -r C:/Desenvolvimento/forensicTolls/Estenografia/relatorio
#

'''
usage: Extração de arquivos escondidos em imagens .. 

python Escarafuncho [-h] [-v] (--md5 | --sha256 | --sha512) -d ROOTPATH -r REPORTPATH

arguments:
  -h, --help          mostra esta mensagem de ajuda e sai do programa
  -v, --verbose       permitir acompanhar as operações do programa
  -d                  especifica o caminho raiz para escarafunchar
  -r                  especifica o caminho onde os relatórios e logs serão gravados 
  e.g.                python escarafuncho.py  -v -d c:\TESTDIR\ -r c:\TESTDIR\
'''

import logging                    # Python Standard Library Logger
import time                       # Python Standard Library time functions
import sys                        # Python Standard Library system specific parameters
import os
import _Escarafuncho   # _extrairArquivoEscondido Support Function Module

if __name__ == '__main__':

    __VERSION__ = '0.1'    
    
    # Process the Command Line Arguments
    _Escarafuncho.ParseCommandLine()

    # Turn on Logging
    logging.basicConfig(filename=os.path.join(_Escarafuncho.gl_args.reportPath,'escarafunchador.log'),level=logging.DEBUG,format='%(asctime)s %(message)s')     


    # Record the Starting Time
    startTime = time.time()
    
    # Record the Welcome Message
    logging.info('')
    logging.info('Bemvindo ao Escarafunchador version 0.1 ... Novo scaneamento iniciado')
    logging.info('')
    _Escarafuncho.DisplayMessage('Bemvindo ao Escarafunchador ... version '+ __VERSION__)

    # Record some information regarding the system
    logging.info('Sistema: '+ sys.platform)
    logging.info('Versão: '+ sys.version)
    
    # Traverse the file system directories and hash the files
    filesProcessed = _Escarafuncho.WalkPath()

    # Record the end time and calculate the duration
    endTime = time.time()
    duration = endTime - startTime

    logging.info('Arquivos Processados: ' + str(filesProcessed) )
    logging.info('Tempo transcorrido: ' + str(duration) + ' segundos')
    logging.info('')
    logging.info('Programa Terminado Normalmente')
    logging.info('')

    _Escarafuncho.DisplayMessage("Fim de execução")
    
    

