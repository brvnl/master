#/usr/bin/sh

cd /home/jduarte/master/crawler/
timestamp=`date +%y%m%d%H%M%S`

logFile1='../../logs/RetrieveArticles.BR.'$timestamp'.log'
(python3 RetrieveArticles.BR.py > $logFile1 &)
pid=$!
wait $pid

# waiting previous process to avoid too much pressure on memory
logFile2='../../logs/RetrieveArticles.US.'$timestamp'.log'
(python3 RetrieveArticles.US.py > $logFile2 &)
pid=$!
wait $pid

logFile3='../../logs/RetrievePrices.'$timestamp'.log'
(python3 RetrievePrices.py > $logFile3 &)
pid=$!
wait $pid

logFile4='../../logs/RetrieveFX.'$timestamp'.log'
(python3 RetrieveFX.py > $logFile4 &)
pid=$!
wait $pid

logFile5='../../logs/RetrieveCommodity.'$timestamp'.log'
(python3 RetrieveCommodity.py > $logFile5 &)

exit 0
