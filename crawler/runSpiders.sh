#/usr/bin/sh

timestamp=`date +%y%m%d%H%M%S`
logFile='../../logs/RetrieveArticles.'$timestamp'.log'
(python RetrieveArticles.py > $logFile &)

exit 0
