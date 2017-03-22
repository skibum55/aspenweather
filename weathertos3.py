def lambda_handler(event, context):
    import boto3
    import boto3.session
    import urllib
    import datetime

    BUCKET = 'aspenweather'
# http://stackoverflow.com/questions/39697604/aws-lambda-handler-error-for-set-contents-from-string-to-upload-in-s3
# http://stackoverflow.com/questions/33577503/how-to-configure-authorization-mechanism-inline-with-boto3
    print "ready to connect S3"
    session = boto3.session.Session(region_name='us-east-2')
    s3client = session.client('s3', config= boto3.session.Config(signature_version='s3v4'))
#    print "connected to download"
#    getResponse = s3client.get_object(Bucket=BUCKET, Key='aspen-summary.htm20170212-165435.htm')
#    print("Done, Get Response body:")
#    print(getResponse['Body'].read())
#    print "connected to upload"
#    putResponse = s3client.put_object(Bucket=BUCKET, Key='encrypt-key', Body=b'foobar')
#    print("Done, Put response body ETag:")
#    print(getResponse['ETag'])
#    print "Completed Upload"
# http://stackoverflow.com/questions/2792650/python3-error-import-error-no-module-name-urllib2
# http://stackoverflow.com/questions/7999935/python-datetime-to-string-without-microsecond-component
    stamp = datetime.datetime.now().strftime("%Y-%m-%d-")
    mountains = ['buttermilk','aspen','snowmass','highlands']
    for i in mountains:
        print("Open Page "+i)
        extension = i+"-summary.html"
        url = "http://weather.aspensnowmass.com/"+extension
        htmlfile = urllib.urlopen(url)
        htmltext = htmlfile.read()
        print(htmltext)
#    page = urllib.urlretrieve("http://weather.aspensnowmass.com/highlands-summary.htm")
#    pageData = page.read()
#    print(pageData)
# https://aws.amazon.com/blogs/compute/content-replication-using-aws-lambda-and-amazon-s3/
        print "Upload page"
        key = stamp+extension
        #http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.put_object
        myResponse = s3client.put_object(Bucket=BUCKET, Key=key, Body=htmltext, ContentType='text/html')
        print(myResponse)
    return
