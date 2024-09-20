docker build --platform linux/amd64 -t secretgpt .

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 623470192157.dkr.ecr.us-east-1.amazonaws.com

docker tag secretgpt:latest 623470192157.dkr.ecr.us-east-1.amazonaws.com/secretgpt:latest

docker push 623470192157.dkr.ecr.us-east-1.amazonaws.com/secretgpt:latest
