#/usr/bin/env bash

SYSLOG="syslog.log"
WEBSERVERPATH="/var/www/html"

#analyze_log.py ${SYSLOG}
./ticky_check.py ${SYSLOG}

convert_html=./csv_to_html.py
filename="user_statistics"

if [ -f "${filename}.csv" ] ;then
   ${convert_html} "${filename}.csv" "${filename}.html"
   mv "${filename}.html" "${WEBSERVERPATH}/${filename}.html"
   echo DONE $filename
fi

filename="error_message"
if [ -f "${filename}.csv" ] ;then
   ${convert_html} "${filename}.csv" "${filename}.html"
   mv "${filename}.html" "${WEBSERVERPATH}/${filename}.html"
   echo DONE $filename
fi

