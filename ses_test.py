import boto3
from botocore.exceptions import ClientError
import logging

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

SENDER = ""
RECEPIENT = ""
CONFIGURATION_SET = "ConfigSet"
AWS_REGION = "us-east-2"
SUBJECT = "Amazon SES Test (SDK for Python)"
CHARSET = "UTF-8"

# body for non html client
BODY_TEXT = ("Amazon SES Test (Python) \r\n"
            "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)"
             )

BODY_HTML = """
    <html>
        <head></head>
        <body>
            <h1>Amazon SES Test (SDK for Python)</h1>
            <p>This email was sent with
                <a href='https://aws.amazon.com/ses/'> Amazon SES </a> using the
                <a href='https://aws.amazon.com/sdk-for-python/'>
                AWS SDK for Python (Boto) </a>.
            </p>
        </body>
    </html>
    """
client = boto3.client('ses', region_name=AWS_REGION)

# try sending the email
try:
    # email contents
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECEPIENT,
            ],
            #CcAddresses, BccAddresses
        },
        Message = {
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text':{
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject':{
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source = SENDER,
    )
    logger.info( f"Email sent to {RECEPIENT}" )
# display error incase of one
except ClientError as e:
    logger.exception( f"Email sending failed for {RECEPIENT}" )
    print( e.response['Error']['Message'])
else:
    print('Email sent! Message ID')
    print(response['MessageId'])



