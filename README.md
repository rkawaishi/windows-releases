## Create or update a lambda function

### Before deploy
```
cd src
pip install -r requirements.txt -t .

cd ..
aws cloudformation package --template-file template.yml --s3-bucket [YOUR S3 BUCKET NAME] --output-template-file packaged-template.yml
```

### Deploy


```
aws cloudformation deploy --template-file package-template.yml --stack-name windows-releases
```
