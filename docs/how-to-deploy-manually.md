## Guide

-   python3.8 -m pip freeze > requirements.txt
-   Sync s3
    `aws s3 sync . s3://nozolan-api-artifacts/marriage-api/  --exclude '*'  --include 'main/*' --include 'config/*'  --include 'scripts/*' --include 'registration/*' --include 'matching/*' --include "manage.py" --include "requirements.txt" --exclude 'main/migrations/*' --exclude 'registration/migrations/*' --exclude 'matching/migrations/*' --exclude 'main/media/*' --exclude '*.pyc'`

-   SSH to API host and sync to s3
    `cd /Documents/nozolan/secrets
ssh -i "nozolan-api.pem" ec2-user@ec2-35-153-32-235.compute-1.amazonaws.com
cd /home/ec2-user/www/nozolan/marriage-api
aws s3 sync s3://nozolan-api-artifacts/marriage-api/ .`

-   `pkill gunicorn`

-   `python3.8 -m pip install -r requirements.txt`

-   Login in to MYSQl local server and create a new database nozolan
    `CREATE DATABASE nozolan CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;`
    `ALTER DATABASE nozolan CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

-   `python3.8 manage.py makemigrations`

-   `python3.8 manage.py migrate`

-   `python3.8 manage.py collectstatic`

-   make sure .env file is created with relevent env variables.

-   `gunicorn -c config/gunicorn/dev.py`

-   `python3.8 /home/ec2-user/www/nozolan/manage.py runserver 0.0.0.0:8001 > /dev/null 2>&1 &`

-   `sudo systemctl restart nginx`

-   python3.8 manage.py crontab add
