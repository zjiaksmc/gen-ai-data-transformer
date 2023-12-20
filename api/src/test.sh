python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
# uname: aidf_admin
# password: 5TkoQ2y-C+^+G5<S
python manage.py runserver 0.0.0.0:5001
uwsgi --ini service.ini

## Deploy API to GCP app engine
gcloud app create --region=us-central --service-account=general-access@docai-warehouse-demo.iam.gserviceaccount.com
gcloud app deploy --quiet

# Testing the API endpoint
## /copilot/chat/session/{session_id}
{
    "message": "write a SQL query to reformat the ssn_org column. Remove all non-numeric charactors. limit output to less than 9 characters."
}
1c39a23811cd43efb4c8867e1181cb61
## /copilot/chat/session
{
    "user_id": "zjia",
    "email": "zjia@resultant.com"
}
## /account/login
{
  "username": "aidf_admin",
  "email": "zjia@resultant.com",
  "password": "5TkoQ2y-C+^+G5<S"
}