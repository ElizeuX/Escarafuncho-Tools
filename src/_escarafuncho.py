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

#
# _extrairArquivoEscondido.py
#

# suporta as funções do escarafuncho, onde o trabalho real é feito
# 
# Display Message()                    ParseCommandLine()                                WalkPath()
# HashFile()                           LogEvents()                                       class _CVSWriter
# ValidateDirectory()                  ValidateDirectoryWritable()                       UnZip_File()
#

import os                                #Python Standard Library - Miscellaneous operating system interfaces
import stat                              #Python Standard Library - constants and functions for interpreting os results
import time                              #Python Standard Library - Time access and conversions functions
import hashlib                           #Python Standard Library - Secure hashes and message digests
import argparse                          #Python Standard Library - Parser for command-line options, arguments
import csv                               #Python Standard Library - reader and writer for csv files
import logging        

import zipfile


log = logging.getLogger('main._escarafuncho')
log.info("I'm here in _escarafuncho!")

#
# Name: ParseCommand() Function
#
# Desc: Process and Validate the command line arguments
#           use Python Standard Library module argparse
#
# Input: none
#  
# Actions: 
#              Uses the standard library argparse to process the command line
#              establishes a global variable gl_args where any of the functions can
#              obtain argument information
#
def ParseCommandLine():

    parser = argparse.ArgumentParser('Python sistema escarafunchador .. escarafuncho')

    # setup a group where the selection is mutually exclusive and required.
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--md5',       help = 'specifies MD5 algorithm',       action='store_true')
    group.add_argument('--sha256',   help = 'specifies SHA256 algorithm',   action='store_true')   
    group.add_argument('--sha512',   help = 'specifies SHA512 algorithm',   action='store_true')   

    parser.add_argument('-v', "--verbose",  help="allows progress messages to be displayed", action='store_true')    
    parser.add_argument('-d', '--rootPath', type= ValidateDirectory, required=True, help="specify the root path for hashing")
    parser.add_argument('-r', '--reportPath', type= ValidateDirectoryWritable, required=True, help="specify the path for reports and logs will be written")   

    # create a global object to hold the validated arguments, these will be available then
    # to all the Functions within the _pfish.py module

    global gl_args    
    global gl_hashType
    
    gl_args = parser.parse_args()    

    if gl_args.md5:
        gl_hashType = 'MD5'
    elif gl_args.sha256:
        gl_hashType = 'SHA256'
    elif gl_args.sha512:
        gl_hashType = 'SHA512'
    else:
        gl_hashType = "Unknown"
        logging.error('Tipo de Hash desconhecido')       
        
    DisplayMessage("Linha de comando processada com sucesso")

    return

# End ParseCommandLine============================================================      

#
# Name: WalkPath() Function
#
# Desc: Walk the path specified on the command line
#           use Python Standard Library module os and sys
#
# Input: none, uses command line arguments
#  
# Actions: 
#              Uses the standard library modules os and sys
#              to traverse the directory structure starting a root
#              path specified by the user.  For each file discovered, WalkPath
#              will call the Function HashFile() to perform the file hashing
#

def WalkPath():

    processCount = 0
    errorCount = 0
    
    oCVS = _CSVWriter(os.path.join(gl_args.reportPath, 'fileSystemReport.csv'), gl_hashType)   
    
    # Create a loop that process all the files starting
    # at the rootPath, all sub-directories will also be
    # processed
    
    log.info('Root Path: ' + gl_args.rootPath)    
    
    for root, dirs, files in os.walk(gl_args.rootPath):    
        # for each file obtain the filename and call the HashFile Function
        for file in files:
            fname = os.path.join(root, file)
            result = UnZip_File(fname, file, oCVS)

            # if hashing was successful then increment the ProcessCount
            if result is True:
                processCount += 1            
            else:
                errorCount += 1       
                
        
    oCVS.writerClose()
        
    return(processCount)

#End WalkPath==================================================


def UnZip_File(theFile, simpleName, o_result):

    tamanhoLinha = 60

    # Verify that the path is valid
    if os.path.exists(theFile):

        #Verify that the path is not a symbolic link
        if not os.path.islink(theFile):

            #Verify that the file is real
            if os.path.isfile(theFile):

                try:

                    theFileStats =  os.stat(theFile)
                    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(theFile)

                    # print the size of the file in Bytes
                    fileSize = str(size)

                    #print MAC Times
                    modifiedTime = time.ctime(mtime)
                    accessTime = time.ctime(atime)
                    createdTime = time.ctime(ctime)
                    
                    ownerID = str(uid)
                    groupID = str(gid)
                    fileMode = bin(mode)

                    f = open(theFile, 'rb')
                    rd = f.read()
                    if gl_args.md5:
                        #Calcuation and Print the MD5
                        hash = hashlib.md5()
                        hash.update(rd)
                        hexMD5 = hash.hexdigest()
                        hashValue = hexMD5.upper()
                    elif gl_args.sha256:
                        hash=hashlib.sha256()
                        hash.update(rd)
                        hexSHA256 = hash.hexdigest()
                        hashValue = hexSHA256.upper()
                    elif gl_args.sha512:
                        #Calculate and Print the SHA512
                        hash=hashlib.sha512()
                        hash.update(rd)
                        hexSHA512 = hash.hexdigest()
                        hashValue = hexSHA512.upper()
                    else:
                        log.error('Hash not Selected')
                    f.close()
                    
                    #Attempt to open the file                                    
                    un_zip = zipfile.ZipFile(theFile)
                    
                except zipfile.BadZipfile:
                    #if open fails não é um zipfile                                        
                    log.warning(theFile + '.' * (tamanhoLinha - len(theFile)) + 'Nada Consta')
                    DisplayMessage(theFile + '.' * (tamanhoLinha - len(theFile)) + 'Nada Consta')
                    o_result.writeCSVRow(simpleName, os.path.dirname(theFile), size, modifiedTime, accessTime, createdTime, hashValue,  ownerID, groupID, mode, 'NADA CONSTA')
                    return True
                else:
                    try:               
                        log.info(theFile + '.' * (tamanhoLinha - len(theFile)) + 'Arquivo suspeito')
                        DisplayMessage(theFile +  '.' * (tamanhoLinha - len(theFile)) + 'Arquivo suspeito')
                        if not os.path.exists(simpleName+'-DESCOMPACTADO'):
                            os.makedirs(simpleName+'-DESCOMPACTADO')                            
                        un_zip.extractall(simpleName+'-DESCOMPACTADO')
                        un_zip.close()
                    except sipfile.BadZipFile:
                        # if read fails, then close the file and report error
                        f.close()
                        log.warning('Descompactação falhou: ' + theFile)
                        return                   
                        
                # write one row to the output file                                        
                o_result.writeCSVRow(simpleName, os.path.dirname(theFile), size, modifiedTime, accessTime, createdTime, hashValue, ownerID, groupID, mode, "ARQUIVO SUSPEITO")
                
                return True
            else:
                log.warning('[' + repr(simpleName) + ', Skipped NOT a File' + ']')
                return False
        else:
            log.warning('[' + repr(simpleName) + ', Skipped Link NOT a File' + ']')
            return False
    else:
            log.warning('[' + repr(simpleName) + ', Path does NOT exist' + ']')        
    return False

# End HashFile Function ===================================

#
# Name: ValidateDirectory Function
#
# Desc: Function that will validate a directory path as 
#           existing and readable.  Used for argument validation only
#
# Input: a directory path string
#  
# Actions: 
#              if valid will return the Directory String
#
#              if invalid it will raise an ArgumentTypeError within argparse
#              which will inturn be reported by argparse to the user
#

def ValidateDirectory(theDir):

    # Validate the path is a directory
    if not os.path.isdir(theDir):
        raise argparse.ArgumentTypeError('Directory does not exist')

    # Validate the path is readable
    if os.access(theDir, os.R_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError('Directory is not readable')

#End ValidateDirectory ===================================

#
# Name: ValidateDirectoryWritable Function
#
# Desc: Function that will validate a directory path as 
#           existing and writable.  Used for argument validation only
#
# Input: a directory path string
#  
# Actions: 
#              if valid will return the Directory String
#
#              if invalid it will raise an ArgumentTypeError within argparse
#              which will inturn be reported by argparse to the user
#

def ValidateDirectoryWritable(theDir):

    # Validate the path is a directory
    if not os.path.isdir(theDir):
        raise argparse.ArgumentTypeError('Directory does not exist')

    # Validate the path is writable
    if os.access(theDir, os.W_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError('Directory is not writable')

#End ValidateDirectoryWritable ===================================


#==================================================

#
# Name: DisplayMessage() Function
#
# Desc: Displays the message if the verbose command line option is present
#
# Input: message type string
#  
# Actions: 
#              Uses the standard library print function to display the messsage
#
def  DisplayMessage(msg):

    if gl_args.verbose:    
        print(msg)

    return   

#End DisplayMessage=====================================

# 
# Class: _CSVWriter 
#
# Desc: Handles all methods related to comma separated value operations
#
# Methods  constructor:     Initializes the CSV File
#                writeCVSRow:   Writes a single row to the csv file
#                writerClose:      Closes the CSV File

class _CSVWriter:

    def __init__(self, fileName, hashType):
        try:
            # create a writer object and then write the header row            
            self.csvFile = open(fileName, 'w')            
            self.writer = csv.writer(self.csvFile, delimiter=';', quoting=csv.QUOTE_ALL, lineterminator='\n')
            self.writer.writerow(('File', 'Path', 'Size', 'Modified Time', 'Access Time', 'Created Time', hashType, 'Owner', 'Group', 'Mode', 'Observação' ))            
        except Exception as e:            
            log.error('CSV File Failure')            

    def writeCSVRow(self, fileName, filePath, fileSize, mTime, aTime, cTime, hashValue, own, grp, mod, observacao):
        self.writer.writerow((fileName, filePath, fileSize, mTime, aTime, cTime, hashValue, own, grp, mod, observacao))

    def writerClose(self):
        self.csvFile.close()
