import subprocess, gzip, glob
import shutil, sys

from calendar   import monthrange
from datetime   import datetime
from sys        import argv
from os         import getcwd, chdir, listdir, remove


def lastDayStrOfPreviousMonth():
    d = date.today() - timedelta( 1 )
    return str( d.month ), str( d.day )


#=================== Mainline of the program =====================

# If only 3 arguments were given, prompt the user for the password.
# Subtract 1 from the number of arguments to account for the script
# name being the first argument in Python.

viceDbName = ''
username   = ''
password   = ''
numArgs    = len( argv ) - 1

if numArgs != 3:
    print ('\nWrong number of command line arguments = ' + str( numArgs ))
    print ('The arguments should be: VICE_database_name, username, password.\n')
    exit
else:
    # Get command line arguments and store into named vars.
    viceDbName = argv[ 1 ]
    username   = argv[ 2 ]
    password   = argv[ 3 ]


# Get the current day, month, and last day of month strings.
curYear   = datetime.now().year
curMonth  = datetime.now().month
curDay    = datetime.now().day
curDayStr = str( curDay   )

curMonthTuple     = monthrange( curYear, curMonth )
lastDayOfMonthStr = str( curMonthTuple[1] )


# Set the current working directory to the dump subdirectory.
dumpDir = getcwd() + r"\dump"
print ("dumpDir: "+dumpDir)
chdir( dumpDir )


# Clear the dump directory used for to store gzip files before they are
# copied to the daily and monthly directories.
# Start by getting a list of all file names or paths in the directory.
oldDumpDirFiles = listdir( dumpDir )
for inFileName in oldDumpDirFiles:
    remove( inFileName )


# Generate an SQL file for all events and routines.
rtnDumpCmd = [ 'mysqldump', '-u' + username, '-p' + password, '--no-data',
               '--events', '--routines', '--single-transaction', 
               '--log-error=routines.log', '--result-file=routines.sql',
               viceDbName ]
print ("rtnDumpCmd: ")
print (rtnDumpCmd )              
subprocess.call( rtnDumpCmd )


# Generate SQL and data (CSV format) files for all tables.
tablesDumpCmd = [ 'mysqldump', '-u' + username, '-p' + password,
                  '--single-transaction', '--add-drop-table',
                  '--log-error=tables.log', '--tab=.', viceDbName ]
#tablesDumpCmd = [ 'mysqldump', '-u' + username, '-p' + password,
#                  '--single-transaction', '--add-drop-table',
#                  '--log-error=tables.log', viceDbName ]
print ("tablesDumpCmd: ")
print (tablesDumpCmd)                  
subprocess.call( tablesDumpCmd )


# Compress all the files using gzip set at max compression (9).
newDumpDirFiles = [ f for f in listdir( dumpDir ) if not f.endswith('.log') ]
print ("newDumpDirFiles: ")
print (newDumpDirFiles)

for inFileName in newDumpDirFiles:
    fIn  = open( inFileName, 'rb' )
    fOut = gzip.open( inFileName + '.gz', 'wb', 9 )
    fOut.writelines( fIn )
    fOut.close()
    fIn.close()

fromDir = getcwd()
print ("fromDir: " + fromDir)

# Get a list of all compressed files in the current working directory.
allFilesToCopy = [ f for f in listdir('.') if f.endswith( '.gz'  ) 
                                           or f.endswith( '.log' ) ]


# Move all the gzipped files to the current day of the month directory.
# Start by constructing the paths to the daily directory,
# which will be relative to the current working directory.
dailyDir = "..\\" + curDayStr + "\\"
print ("dailyDir: "+dailyDir)
chdir( dailyDir )
# Clear all the old files from the daily directory.
oldGzipFiles = listdir( dailyDir )
for inFileName in oldGzipFiles:
    print ( "file name :" + inFileName)
    remove( inFileName )
# Copy the gzipped files to the daily directory. 
chdir( fromDir )
for f in allFilesToCopy:
    shutil.copy2( f, dailyDir )
    print( "copying file: " + f)

# Is today the last day of the month? If so, copy the compressed files to
# the current month subdirectory of the months directory.
if curDayStr == lastDayOfMonthStr:
    curMonthStr = str( curMonth )
    monthlyDir  = "..\\months\\" + curMonthStr + "\\"
    for f in allFilesToCopy:
        shutil.copy2( f, monthlyDir )

