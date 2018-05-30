echo "Start VICE backup..."
cd c:\VICE_backup
set a=.v2.sql
set b=.v2.zip
set year=%date:~10,4%
set month=%date:~4,2%
set day=%date:~7,2%
set fileName=%year%_%month%_%day%%a%
set zipFileName=%year%_%month%_%day%%b%
echo %fileName%
mysqldump.exe -u vice_backup -pglcmdvice123 --skip-triggers v2> %fileName%
"C:\Program Files\7-Zip\7z.exe" a -tzip %zipFileName% %fileName%
del %fileName%
