#
# _escarafuncho.py
#

# pfish support functions, where all the real work gets done
# 
# Display Message()                    ParseCommandLine()                                WalkPath()
# LogEvents()                          class _CVSWriter
# ValidateDirectory()                  ValidateDirectoryWritable()                       UnZip_File() 
#

import os                                 #Python Standard Library - Miscellaneous operating system interfaces
import stat                               #Python Standard Library - constants and functions for interpreting os results
import time                              #Python Standard Library - Time access and conversions functions
import argparse                        #Python Standard Library - Parser for command-line options, arguments
import csv                                 #Python Standard Library - reader and writer for csv files
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

    parser.add_argument('-v', "--verbose",  help="allows progress messages to be displayed", action='store_true')    
    parser.add_argument('-d', '--rootPath', type= ValidateDirectory, required=True, help="specify the root path for hashing")
    parser.add_argument('-r', '--reportPath', type= ValidateDirectoryWritable, required=True, help="specify the path for reports and logs will be written")   

    # create a global object to hold the validated arguments, these will be available then
    # to all the Functions within the _pfish.py module

    global gl_args    
    
    gl_args = parser.parse_args()           
        
    DisplayMessage("Command line processed: Successfully")

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
    
    oCVS = _CSVWriter(os.path.join(gl_args.reportPath, 'fileSystemReport.csv') )   
    
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

                    #Attempt to open the file                                    
                    un_zip = zipfile.ZipFile(theFile)
                    
                    #Print the simple file name
                    DisplayMessage("Descompactando: " + theFile)                   
                    
                except zipfile.BadZipfile:
                    #if open fails não é um zipfile                    
                    log.warning(theFile + '...Nada Consta')
                    DisplayMessage(theFile + '..Nada Consta')
                    o_result.writeCSVRow(simpleName, theFile, size, modifiedTime, accessTime, createdTime, ownerID, groupID, mode, 'NADA CONSTA')
                    return True
                else:
                    try:               
                        log.info(theFile + "\tArquivo suspeito")                                 
                        if not os.path.exists('tmp'):
                            os.makedirs('tmp')
                        un_zip.extractall('tmp')
                        un_zip.close()
                    except sipfile.BadZipFile:
                        # if read fails, then close the file and report error
                        f.close()
                        log.warning('Descompactação falhou: ' + theFile)
                        return                   
                        
                # write one row to the output file                                        
                o_result.writeCSVRow(simpleName, theFile, size, modifiedTime, accessTime, createdTime, ownerID, groupID, mode, "ARQUIVO SUSPEITO")
                
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

    def __init__(self, fileName):
        try:
            # create a writer object and then write the header row            
            self.csvFile = open(fileName, 'w')            
            self.writer = csv.writer(self.csvFile, delimiter=';', quoting=csv.QUOTE_ALL)
            self.writer.writerow(('File', 'Path', 'Size', 'Modified Time', 'Access Time', 'Created Time', 'Owner', 'Group', 'Mode', 'Observação' ))            
        except Exception as e:            
            log.error('CSV File Failure')            

    def writeCSVRow(self, fileName, filePath, fileSize, mTime, aTime, cTime, own, grp, mod, observacao):                
        self.writer.writerow((fileName, filePath, fileSize, mTime, aTime, cTime,  own, grp, mod, observacao))                        

    def writerClose(self):
        self.csvFile.close()
