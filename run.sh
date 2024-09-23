sed -i '' 's/DJANGO_ENV="prod"/DJANGO_ENV="dev"/'  /Users/abdel/Documents/ai/api/main/settings/.env
kill -9 $(lsof -i:8000 -t) 2> /dev/null
python3.12 manage.py runserver 0.0.0.0:8000