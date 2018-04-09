echo "Start backup..."
cd c:\backup
set a=.myDB.sql
set year=%date:~10,4%
set month=%date:~4,2%
set day=%date:~7,2%
set fileName=%year%_%month%_%day%%a%
echo %fileName%
mysqldump.exe -u root -p --skip-triggers myDB > %fileName%
