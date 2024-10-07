create request layer using docker amazon ec2 instance. mac does not work properly

aws lambda publish-layer-version \
 --layer-name requests-layer \
 --description "A layer with requests" \
 --zip-file fileb://requests-layer.zip \
 --compatible-runtimes python3.12

arn:aws:lambda:us-east-1:623470192157:layer:requests-layer:3

curl --no-buffer -X POST https://v0zbn4tgch.execute-api.us-east-1.amazonaws.com/default/aiTicket \
-H "Content-Type: application/json" \
-d '{"prompt": "how to create a new user?"}'
