from inspect import getmembers, ismethod

from .message import (JMSMessageType, _add_required_message_attribute_names,
                      _create_jms_message, _encode_jms_message,
                      _encode_jms_messages)


class JMSQueue(object):

  def __init__(self, sqs_queue):
    assert sqs_queue, 'sqs_queue cannot be None'
    assert sqs_queue.__class__.__module__ == 'boto3.resources.factory' and sqs_queue.__class__.__name__ == 'sqs.Queue', 'sqs_queue must be of type boto3.resources.factory.sqs.Queue'
    self.__sqs_queue = sqs_queue
    self.attributes = sqs_queue.attributes
    self.dead_letter_source_queues = sqs_queue.dead_letter_source_queues
    self.url = sqs_queue.url
    for method in getmembers(sqs_queue, ismethod):
      if not method[0].startswith('_') and method[0] not in ['receive_messages', 'send_message', 'send_messages']:
        setattr(self, method[0], method[1])


  def __get_sqs_queue(self):
    return self.__sqs_queue


  sqs_queue = property(__get_sqs_queue)


  def receive_jms_messages(self, **kwargs):
    kwargs['MessageAttributeNames'] = _add_required_message_attribute_names(kwargs.get('MessageAttributeNames') or [])
    return [ _create_jms_message(sqs_message) for sqs_message in self.sqs_queue.receive_messages(**kwargs) ]


  def send_bytes_message(self, JMSReplyTo=None, JMSCorrelationId=None, **kwargs):
    return self.sqs_queue.send_message(
      **_encode_jms_message(
        JMSMessageType=JMSMessageType.BYTE, 
        JMSReplyTo=JMSReplyTo, 
        JMSCorrelationId=JMSCorrelationId, 
        **kwargs)
    )


  def send_jms_messages(self, **kwargs):
    return self.sqs_queue.send_messages(**_encode_jms_messages(**kwargs))


  def send_text_message(self, JMSReplyTo=None, JMSCorrelationId=None, **kwargs):
    return self.sqs_queue.send_message(
      **_encode_jms_message(
        JMSMessageType=JMSMessageType.TEXT, 
        JMSReplyTo=JMSReplyTo, 
        JMSCorrelationId=JMSCorrelationId, 
        **kwargs
      )
    )
