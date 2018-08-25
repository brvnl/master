#/usr/bin/sh

cd /home/jduarte/master/crawler/
timestamp=`date +%y%m%d%H%M%S`
logFile='../../logs/RetrieveArticles.'$timestamp'.log'
#(python RetrieveArticles.PROD.py > $logFile &)
(python3 RetrieveArticles.PROD.3.py > $logFile &)
exit 0
