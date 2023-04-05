#################################################################################################################
#This Script monitors CP4D URL via REST API call
#Author - rraghavan

#################################################################################################################
Logger()
{
 echo `date` "=>" $1  | tee  -a $ScriptLog
}

#####
#Main
##########
date_time=`date +"%m%d%y_%H%M%S"`

Log_Dir=`pwd`/logs
ScriptLog="$Log_Dir/curl_log_${date_time}"
touch $ScriptLog


Subject="CP4D CRITICAL ALERT"
from="dspdev@illumina.com"
to="rraghavan@illumina.com,cjayachandran@illumina.com"

# set URLs to check:
url1="https://dspdev.illumina.com"

# check HTTP return codes (3 sec timeout)
url1Status=`curl -IsSkL -m 3 --head $url1 --write-out %{http_code} --output /dev/null`

#####################################
# Alerting via email #
#####################################
Logger "\n$url1 returned $url1Status\n"

# If ALL URLs are not reachable, send email notification and exit script
if [[ $url1Status -ne 200 ]]
  then
  Logger "Cannot reach the IBM Cloud Pak for Data URL $url1\n"
  body="Cannot reach the IBM Cloud Pak for Data URL $url1"
  echo -e "Subject:${subject}\n${body}" | sendmail -f "${from}" -t "${to}"

  exit 1

# Else send email notification for any URLs not reachable
else
  Logger "Post Install file present, exiting the script....."
fi

exit 0
