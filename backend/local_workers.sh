#! /bin/sh
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env." 
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
if [ -d ".env" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run local_setup.sh first"
    exit 1
fi

# Activate virtual env
. .env/bin/activate
export ENV=development
celery -A main.celery worker -l info
# deactivate