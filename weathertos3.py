def lambda_handler(event, context):
    import boto3
    import boto3.session
    
    BUCKET = 'aspenweather'
# http://stackoverflow.com/questions/39697604/aws-lambda-handler-error-for-set-contents-from-string-to-upload-in-s3
# http://stackoverflow.com/questions/33577503/how-to-configure-authorization-mechanism-inline-with-boto3
    print "ready to connect S3"
    session = boto3.session.Session(region_name='us-east-2')
    s3client = session.client('s3', config= boto3.session.Config(signature_version='s3v4'))
    print "connected to download"
    getResponse = s3client.get_object(Bucket=BUCKET, Key='aspen-summary.htm20170212-165435.htm')
    print("Done, Get Response body:")
    print(getResponse['Body'].read())
    print "connected to upload"
    putResponse = s3client.put_object(Bucket=BUCKET, Key='encrypt-key',Body=b'foobar',)
    print("Done, Put response body ETag:")
    print(getResponse['ETag'])
    print "Completed Upload"
    return
