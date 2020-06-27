from base64 import b64decode, b64encode
from enum import Enum
from inspect import getmembers, ismethod

from .constants import *


def _create_string_attribute(value):
  return {
    'DataType': 'String',
    'StringValue': str(value)
  }


def _get_string_attribute(value):
  assert value['DataType'] == 'String'
  return value['StringValue']


def _add_required_message_attribute_names(message_attribute_names):
  assert isinstance(message_attribute_names, list), 'MessageAttributeNames must be a list'
  return list(
    set(message_attribute_names) | 
    set([JMS_SQS_CORRELATION_ID, JMS_SQS_REPLY_TO_QUEUE_NAME, JMS_SQS_REPLY_TO_QUEUE_URL, JMS_SQS_MESSAGE_TYPE])
  ) if 'All' not in message_attribute_names and '.*' not in message_attribute_names else message_attribute_names


def _encode_jms_message(JMSMessageType=None, JMSReplyTo=None, JMSCorrelationId=None, **kwargs):
  kwargs['MessageAttributes'] = kwargs.get('MessageAttributes', {})
  if JMSMessageType == JMSMessageType.BYTE:
    assert isinstance(kwargs.get('MessageBody'), (bytes, bytearray)), 'MessageBody must be bytes or bytearray'
    kwargs['MessageBody'] = b64encode(kwargs['MessageBody']).decode()
  elif JMSMessageType != JMSMessageType.TEXT:
    raise ValueError('JMSMessageType must be JMSMessageType.BYTE or JMSMessageType.TEXT')
  kwargs['MessageAttributes'][JMS_SQS_MESSAGE_TYPE] = _create_string_attribute(JMSMessageType.value)
  if JMSReplyTo:
    assert isinstance(JMSReplyTo, dict) and QUEUE_NAME in JMSReplyTo and QUEUE_URL in JMSReplyTo, 'JMSReplyTo must be a dict and must contain QueueName and QueueUrl'
    kwargs['MessageAttributes'][JMS_SQS_REPLY_TO_QUEUE_NAME] = _create_string_attribute(JMSReplyTo[QUEUE_NAME])
    kwargs['MessageAttributes'][JMS_SQS_REPLY_TO_QUEUE_URL] = _create_string_attribute(JMSReplyTo[QUEUE_URL])
  if JMSCorrelationId:
    assert isinstance(JMSCorrelationId, str), 'JMSCorrelationId must be a str'
    kwargs['MessageAttributes'][JMS_SQS_CORRELATION_ID] = _create_string_attribute(JMSCorrelationId)
  return kwargs


def _encode_jms_messages(**kwargs):
  entries = kwargs['Entries']
  for entry in entries:
    entry['MessageAttributes'] = entry.get('MessageAttributes', {})
    if JMS_MESSAGE_TYPE in entry:
      jms_message_type = entry.pop(JMS_MESSAGE_TYPE)
      if jms_message_type == JMSMessageType.BYTE.value:
        assert isinstance(entry.get('MessageBody'), (bytes, bytearray)), 'MessageBody must be bytes or bytearray'
        entry['MessageBody'] = b64encode(entry['MessageBody']).decode()
      elif jms_message_type != JMSMessageType.TEXT.value:
        raise ValueError('JMSMessageType must be {} or {}'.format(JMSMessageType.BYTE.value, JMSMessageType.TEXT.value))
      entry['MessageAttributes'][JMS_SQS_MESSAGE_TYPE] = _create_string_attribute(jms_message_type)
    if JMS_REPLY_TO in entry:
      jms_reply_to = entry.pop(JMS_REPLY_TO)
      assert isinstance(jms_reply_to, dict) and QUEUE_NAME in jms_reply_to and QUEUE_URL in jms_reply_to, 'JMSReplyTo must be a dict and must contain QueueName and QueueUrl'
      entry['MessageAttributes'][JMS_SQS_REPLY_TO_QUEUE_NAME] = _create_string_attribute(jms_reply_to[QUEUE_NAME])
      entry['MessageAttributes'][JMS_SQS_REPLY_TO_QUEUE_URL] = _create_string_attribute(jms_reply_to[QUEUE_URL])
    if JMS_CORRELATION_ID in entry:
      jms_correlation_id = entry.pop(JMS_CORRELATION_ID)
      assert isinstance(jms_correlation_id, str), 'JMSCorrelationId must be a str'
      entry['MessageAttributes'][JMS_SQS_CORRELATION_ID] = _create_string_attribute(jms_correlation_id)
    assert JMS_SQS_MESSAGE_TYPE in entry['MessageAttributes'] and _get_string_attribute(entry['MessageAttributes'][JMS_SQS_MESSAGE_TYPE])  in (JMSMessageType.BYTE.value, JMSMessageType.TEXT.value), '{} must be either {} or {}'.format(JMS_SQS_MESSAGE_TYPE, JMSMessageType.BYTE.value, JMSMessageType.TEXT.value)
  return kwargs


def _create_jms_message(sqs_message):
  return JMSBytesMessage(sqs_message) \
    if JMSMessageType.get(sqs_message.message_attributes.get(JMS_SQS_MESSAGE_TYPE)) == JMSMessageType.BYTE \
      else JMSTextMessage(sqs_message)


class JMSMessageType(Enum):
  BYTE = 'byte'
  TEXT = 'text'


  @classmethod
  def get(cls, value):
    if value == cls.BYTE.value:
      return cls.BYTE
    elif value == cls.TEXT.value:
      return cls.TEXT
    else:
      raise ValueError('Unknown JMS message type: {}'.format(value))


class JMSMessage(object):

  def __init__(self, sqs_message):
    assert sqs_message, 'message cannot be None'
    assert sqs_message.__class__.__module__ == 'boto3.resources.factory' and sqs_message.__class__.__name__ == 'sqs.Message', \
      'message must be of type boto3.resources.factory.sqs.Message'
    self.__sqs_message = sqs_message
    self.attributes = sqs_message.attributes
    self.md5_of_body = sqs_message.md5_of_body
    self.md5_of_message_attributes = sqs_message.md5_of_message_attributes
    self.message_id = sqs_message.message_id
    self.queue_url = sqs_message.queue_url
    self.receipt_handle = sqs_message.receipt_handle
    for method in getmembers(sqs_message, ismethod):
      if not method[0].startswith('_') and method[0] not in ['get_available_subresources', 'Queue']:
        setattr(self, method[0], method[1])


  def _get_body(self):
    return self.sqs_message.body


  def __get_jms_correlation_id(self):
    correlation_id_attribute = self.__sqs_message.message_attributes.get(JMS_SQS_CORRELATION_ID)
    return _get_string_attribute(correlation_id_attribute) if correlation_id_attribute else None


  def __get_jms_message_type(self):
    return JMSMessageType.get(_get_string_attribute(self.__sqs_message.message_attributes[JMS_SQS_MESSAGE_TYPE]))


  def __get_jms_reply_to(self):
    message_attributes = self.__sqs_message.message_attributes
    return {
      QUEUE_NAME: _get_string_attribute(message_attributes[JMS_SQS_REPLY_TO_QUEUE_NAME]),
      QUEUE_URL: _get_string_attribute(message_attributes[JMS_SQS_REPLY_TO_QUEUE_URL])
    } if JMS_SQS_REPLY_TO_QUEUE_NAME in message_attributes and JMS_SQS_REPLY_TO_QUEUE_URL in message_attributes else None
  

  def __get_message(self):
    return self.__sqs_message


  def __get_message_attributes(self):
    message_attributes = self.__sqs_message.message_attributes
    message_attributes.pop(JMS_SQS_MESSAGE_TYPE, None)
    message_attributes.pop(JMS_SQS_CORRELATION_ID, None)
    message_attributes.pop(JMS_SQS_REPLY_TO_QUEUE_NAME, None)
    message_attributes.pop(JMS_SQS_REPLY_TO_QUEUE_URL, None)
    return message_attributes


  sqs_message = property(__get_message)
  body = property(_get_body)
  jms_correlation_id = property(__get_jms_correlation_id)
  jms_message_type = property(__get_jms_message_type)
  jms_reply_to = property(__get_jms_reply_to)
  message_attributes = property(__get_message_attributes)


  def get_available_subresources(self):
    return ['JMSQueue']


  def Queue(self):
    from .resource import JMSQueue
    return JMSQueue(self.sqs_message.Queue())


class JMSBytesMessage(JMSMessage):

  def __init__(self, sqs_message):
    super().__init__(sqs_message)

  
  def _get_body(self):
    return b64decode(super()._get_body())


class JMSTextMessage(JMSMessage):

  def __init__(self, sqs_message):
    super().__init__(sqs_message)
