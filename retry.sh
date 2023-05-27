##
# retry.sh
# Provides utility function commonly needed across Cloud Build pipelines to
# retry commands on failure.
#
# Usage:
# 1. Retry single command:
#
# ./retry.sh "CMD"
#
# 2. Retry with check:
#
# ./retry.sh "gcloud RESOURCE EXISTS?" "gcloud ACTION"
#
#
# Note:
#   $# - the number of command-line arguments passed
#   $? - the exit value of the last command
##

# Usage: try "cmd1" "cmd2"
# If first cmd executes successfully then execute second cmd
runIfSuccessful() {
  echo "running: $1"
  $($1 > /dev/null)
  if [ $? -eq 0 ]; then
    echo "running: $2"
    $($2 > /dev/null)
  else return 1
  fi
}

# Define max retries
max_attempts=3;
attempt_num=1;
seconds="${WAIT:=2}"
arg1="$1"
arg2="$2"

if [ $# -eq 1 ]
then
  cmd="$arg1"
else
  cmd="runIfSuccessful \"$arg1\" \"$arg2\""
fi

until eval $cmd
do
    if ((attempt_num==max_attempts))
    then
        echo "Attempt $attempt_num / $max_attempts failed! No more retries left!"
        exit 1
    else
        echo "Attempt $attempt_num / $max_attempts failed!"
        sleep $(( seconds*attempt_num++ ))
    fi
done
