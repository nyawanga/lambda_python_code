import boto3
from botocore.exceptions import ClientError
import logging


logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

def insert_item(event, context):
    try:
        table = dynamodb.Table('registeruser')
        item = {
            "first_name" : event["fname"],
            "last_name" : event["lname"],
            "emailid" : event["emailid"],
            "mobile_no" : event["mphone"],
            "otp" : event["otp"],
            "username" : event["uname"],
            "password" : event["passwd"],
            "confirm_password" : event["cpasswd"]
            }
        response = table.put_item(Item=item)
        logger.info( f"Added item to dynamodb" )
    except ClientError:
        logger.exception( f"failed to insert data" )
    else:
        return response

def read_item(event, context):
    try:
        Table = dynamodb.Table('registeruser')
        response = Table.get_item()
        logger.info( f"Got items from table" )
    except ClientError :
        logger.exception( "Error fetching data from {Table.arn}" )
    else :
        return response