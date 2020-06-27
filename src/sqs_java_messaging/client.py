from base64 import b64decode
from inspect import getmembers, ismethod

from .constants import *
from .message import (JMSMessageType, _add_required_message_attribute_names,
                      _encode_jms_message, _encode_jms_messages,
                      _get_string_attribute)


class JMSClient(object):

  
  def __init__(self, sqs_client):
    assert sqs_client, 'sqs_client cannot be None'
    assert sqs_client.__class__.__module__ == 'botocore.client' and sqs_client.__class__.__name__ == 'SQS', 'sqs_client must be of type botocore.client.SQS'
    self.__sqs_client = sqs_client
    for method in getmembers(sqs_client, ismethod):
      if not method[0].startswith('_') and method[0] not in ['receive_message', 'send_message', 'send_message_batch']:
        setattr(self, method[0], method[1])


  def __get_sqs_client(self):
    return self.__sqs_client


  sqs_client = property(__get_sqs_client)


  def receive_jms_message(self, **kwargs):
    kwargs['MessageAttributeNames'] = _add_required_message_attribute_names(kwargs.get('MessageAttributeNames') or [])
    response = self.sqs_client.receive_message(**kwargs)
    messages = response.get('Messages')
    if messages:
      for message in messages:
        if JMS_SQS_MESSAGE_TYPE not in message['MessageAttributes']:
          raise ValueError('Message missing attribute {}'.format(JMS_SQS_MESSAGE_TYPE))
        message_type = JMSMessageType.get(_get_string_attribute(message['MessageAttributes'].pop(JMS_SQS_MESSAGE_TYPE)))
        if message_type == JMSMessageType.BYTE:
          message['Body'] = b64decode(message['Body'])
        message[JMS_MESSAGE_TYPE] = message_type
        if JMS_SQS_CORRELATION_ID in message['MessageAttributes']:
          message[JMS_CORRELATION_ID] = _get_string_attribute(message['MessageAttributes'].pop(JMS_SQS_CORRELATION_ID))
        if JMS_SQS_REPLY_TO_QUEUE_NAME in message['MessageAttributes'] and JMS_SQS_REPLY_TO_QUEUE_URL in message['MessageAttributes']:
          message[JMS_REPLY_TO] = {}
          message[JMS_REPLY_TO][QUEUE_NAME] = _get_string_attribute(message['MessageAttributes'].pop(JMS_SQS_REPLY_TO_QUEUE_NAME))
          message[JMS_REPLY_TO][QUEUE_URL] = _get_string_attribute(message['MessageAttributes'].pop(JMS_SQS_REPLY_TO_QUEUE_URL))
    return response


  def send_bytes_message(self, JMSReplyTo=None, JMSCorrelationId=None, **kwargs):
    return self.sqs_client.send_message(**_encode_jms_message(JMSMessageType=JMSMessageType.BYTE, JMSReplyTo=JMSReplyTo, JMSCorrelationId=JMSCorrelationId, **kwargs))


  def send_jms_message_batch(self, **kwargs):
    return self.sqs_client.send_message_batch(**_encode_jms_messages(**kwargs))


  def send_text_message(self, JMSReplyTo=None, JMSCorrelationId=None, **kwargs):
    return self.sqs_client.send_message(**_encode_jms_message(JMSMessageType=JMSMessageType.TEXT, JMSReplyTo=JMSReplyTo, JMSCorrelationId=JMSCorrelationId, **kwargs))
