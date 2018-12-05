import os.path
import sys
import gzip
import shutil
import logging
from datetime import datetime, timedelta


now = datetime.now()
log_filename = now.strftime("%Y%m%d") + ".log"  # i.g.  20181015.log
logging.basicConfig(filename=log_filename, level=logging.INFO)
logging.info("")
logging.info("log file daily compress and clean start at: " + now.strftime("%Y/%m/%d %H:%M:%S"))

if len(sys.argv) < 3:
    print ("need two parameters.\n"
           "i.g. dailylogcc.exe c:\log 14\n"
           "parameter1 is log folder\n"
           "parameter2 is days ago to clean gz file")
    logging.error("need 2 parameter for log daily compress and clean.")
    sys.exit(1)

logfolder = sys.argv[1]
logging.info("log folder: " + logfolder)

logging.info("seeking for *.log and *.log.gz")

days_ago = int(sys.argv[2])

log_date_1days_ago = datetime.now() - timedelta(1)  # keep today's log
gz_date_days_ago = datetime.now() - timedelta(days=days_ago)  # clean n days ago *.log.gz

logging.info("pass today's log: clean last modify date before " + log_date_1days_ago.strftime("%Y/%m/%d %H:%M:%S"))
logging.info("*.log.gz to clean " + str(days_ago) + " days ago : modify before " + gz_date_days_ago.strftime(
    "%Y/%m/%d %H:%M:%S"))
logging.info("-------------")

logfilecount = 0
gzfilecount = 0
bypassfilecount = 0

for dirpath, dirnames, filenames in os.walk(logfolder):
    for filename in filenames:
        if filename.endswith(".log"):
            logfile = os.path.join(dirpath, filename)
            if datetime.utcfromtimestamp(os.path.getmtime(logfile)) < log_date_1days_ago:
                logfilecount += 1

                logging.info("compress: " + logfile)
                with open(logfile, 'rb') as f_in, gzip.open(logfile + '.gz', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                try:
                    os.remove(logfile)
                except OSError as e:
                    logging.error("Error: %s - %s." % (e.filename, e.strerror))
            else:
                bypassfilecount += 1

        if filename.endswith(".log.gz"):
            gzfile = os.path.join(dirpath, filename)
            if datetime.utcfromtimestamp(os.path.getmtime(gzfile)) < gz_date_days_ago:
                os.remove(gzfile)
                logging.info("gz clean: " + gzfile)
                gzfilecount += 1

logging.info("-------------")
logging.info("daily log compress and clean end at: " + datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
logging.info("bypass file(today's log) count is: " + str(bypassfilecount))
logging.info("process file(compress log) count is: " + str(logfilecount))
logging.info("process file(gz log clean) count is: " + str(gzfilecount))

