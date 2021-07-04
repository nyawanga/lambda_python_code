

# https://docs.aws.amazon.com/code-samples/latest/catalog/python-sns-sns_basics.py.html
import logging
import time
import boto3
from botocore.endpoint import Endpoint
from botocore.exceptions import ClientError

logging.basicConfig(filename="snstest.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class SNSWrapper:

    def __init__(self, resource):
        self.sns = resource

    def list_topics(self):
        """
        Lists topics for the current account.

        :return: An iterator that yields the topics.
        """
        try:
            topics = self.sns.topics.all()
            logger.info("Got topics")
        except ClientError as e:
            print(f'cant get topics with err')
            print( e.response["Error"]["Message"] )
        else:
            return topics

    def create_topic(self, name):
        try:
            topic = self.sns.create_topic(Name=name)                                # Warning! this methods only accepts keyword arguements
            logger.info( f"created a topic {name} with ARN {topic.arn}" )
        except ClientError as e:
            logger.exception( 'got error while creating topic {name} ')
            print( e.response["Error"]["Message"] )
            # raise
        except Exception as e:
            print( e )
        else:
            return topic
        
    @staticmethod
    def delete_topic(topic):

        try:
            topic.delete()
            logger.info(f'deleting topic with arn {topic.arn}')
        except ClientError as e:
            logger.exception( f'could not delet topic {topic.arn}' )
            raise

    @staticmethod
    def subscribe(topic,protocol,endpoint):

        try:
            subscription = topic.subscribe(
                Protocol=protocol, Endpoint=endpoint, ReturnSubscriotionArn=True
            )
            logger.info( f'Subscribed {protocol} {endpoint} to {topic.arn}' )
        except ClientError as e:
            logger.exception( f"couldn't subscribe {protocol} {endpoint} to {topic.arn}" )
            raise
        else:
            return subscription

    def list_subscriptions(self,topic=None):
        """
        Lists subscriptions for the current account, optionally limited to a
        specific topic.

        :param topic: When specified, only subscriptions to this topic are returned.
        :return: An iterator that yields the subscriptions.
        """
        try:
            if topic:
                subscriptions = topic.subscriptions.all()
            else:
                subscriptions = self.sns.subscriptions.all()
            logger.info( 'got subscriptions' )
        except ClientError as e:
            logger.exception( f"couldn't get subscriptions" )
            raise
        else:
            return subscriptions
            # while subscriptions :
                # next(subscriptions)

    @staticmethod
    def add_subscription_filter(subscription, attributes):
        """
        Adds a filter policy to a subscription. A filter policy is a key and a
        list of values that are allowed. When a message is published, it must have an
        attribute that passes the filter or it will not be sent to the subscription.

        :param subscription: The subscription the filter policy is attached to.
        :param attributes: A dictionary of key-value pairs that define the filter.
        """
        try:
            att_policy = {key: [value] for key, value in attributes.items()}
            subscription.set_attributes(
                AttributeName='FilterPolicy', AttributeValue=json.dumps(att_policy))
            logger.info("Added filter to subscription %s.", subscription.arn)
        except ClientError:
            logger.exception(
                "Couldn't add filter to subscription %s.", subscription.arn)
            raise

    @staticmethod
    def delete_subscription(subscription):
        """
        Unscubscribes and deletes a subscription
        """

        try:
            subscription.delete()
            logger.info( f'deleted {subscription.arn}')
        except ClientError as e:
            logger.exception( f"couldn't delete {subscription.arn}")
            raise

    def publish_text_message(self, phone_number, message):
        """
        Publishes a text message directly to a phone number without need for a
        subscription.

        :param phone_number: The phone number that receives the message. This must be
                             in E.164 format. For example, a United States phone
                             number might be +12065550101.
        :param message: The message to send.
        :return: The ID of the message.
        """
        try:
            response = self.sns.meta.client.publish(
                PhoneNumber = phone_number, Message = message
            )
            message_id = response["MessageId"]
            logger.info( f"Published message to {phone_number}")
        except ClientError as e:
            logger.exception( f"Couldn't publish message to {phone_number}")
            raise
        else:
            return message_id


sns = SNSWrapper( boto3.resource('sns') )
topic_name = f'demo-basics-topic-{time.time_ns()}'

print(f"Creating topic {topic_name}.")
topic = sns.create_topic(topic_name)
topic_subscriptions = sns.list_subscriptions(topic=topic)
phone_number = '+254xxxxxxxxx'

print(f"Sending an SMS message directly from SNS to {phone_number}.")

sns.publish_text_message(phone_number, 'Hello from the SNS demo!')

print( "\r\n printing topics \r\n " )
for t in sns.list_topics() :
    print( t.arn )

print( "\r\n printing subscriptions \r\n" )
for i in sns.list_subscriptions():
    print(i.arn )

print( f"deleting subscriptions and topic {topic_name}" )
for sub in topic_subscriptions:
    sns.delete_subscription(sub)
sns.delete_topic(topic)


