## Create or update a lambda function

### Before deploy
```
aws cloudformation package --template-file template.yml --s3-bucket [YOUR S3 BUCKET NAME] --output-template-file packaged-template.yml
```

### Deploy


```
aws cloudformation deploy --template-file package-template.yml --stack-name windows-releases
```
