# sqs-java-messaging

### Implements the functionality of [amazon-sqs-java-messaging-lib](https://github.com/awslabs/amazon-sqs-java-messaging-lib) in Python

## Installation
```
pip install sqs-java-messaging
```

## Overview
This library supports `byte` and `text` messages in the AWS SQS Java Messaging Library format. It does **not** support `object` messages.

## API
*   **`sqs_java_messaging.client.JMSClient`**

    ```
    import boto3
    from sqs_java_messaging.client import JMSClient

    client = JMSClient(boto3.client('sqs'))
    ```

    This class wraps [`SQS.Client`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#client) objects. It provides all of the methods of those objects directly ***except*** `receive_message`, `send_message` and `send_message_batch`. These are replaced with `receive_jms_message`, `send_bytes_message`, `send_text_message` and
    `send_jms_message_batch`. 
    
    Once created it may be used exactly as the wrapped `SQS.Client` object.

    *   `receive_jms_message(**kwargs)`

        **Request**
        
        Exactly as [`receive_message`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.receive_message).

        **Response**

        ```
        {
          'Messages': [
            {
              'MessageId': 'string',
              'ReceiptHandle': 'string',
              'MD5OfBody': 'string',
              'Body': 'string' | b'bytes',
              'Attributes': {
                'string': 'string'
              },
              'MD5OfMessageAttributes': 'string',
              'MessageAttributes': {
                'string': {
                  'StringValue': 'string',
                  'BinaryValue': b'bytes',
                  'StringListValues': [
                    'string',
                  ],
                  'BinaryListValues': [
                    b'bytes',
                  ],
                  'DataType': 'string'
                }
              },
              'JMSMessageType': 'byte' | 'text',
              'JMSCorrelationId': 'string',
              'JMSReplyTo': {
                'QueueName': 'string',
                'QueueUrl': 'string'
              }
            },
          ]
        }
        ```

    *   `send_bytes_message(JMSReplyTo=None, JMSCorrelationId=None, **kwargs)`

        **Request**
        
        The same as [`send_message`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.send_message) with the following changes:

        ```
        response = client.send_bytes_message(
          JMSReplyTo={
            'QueueName': 'string',
            'QueueUrl': 'string'
          },
          JMSCorrelationId='string',
          MessageBody=b'bytes' | bytearry,
          ...
        )
        ```

        **Response**

        The same as [`send_message`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.send_message)

    *   `send_jms_message_batch(**kwargs)`

        **Request**

        The same as [`send_message_batch`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.send_message_batch) with the additon of `JMSMessageType`, `JMSCorrelationId` and `JMSReplyTo` and a modification of `MessageBody`.

        ```
        response = client.send_jms_message_batch(
          QueueUrl='string',
          Entries=[
            {
              'Id': 'string',
              'MessageBody': 'string' | b'bytes' | bytearry,
              'DelaySeconds': 123,
              'MessageAttributes': {
                'string': {
                  'StringValue': 'string',
                  'BinaryValue': b'bytes',
                  'StringListValues': [
                    'string',
                  ],
                  'BinaryListValues': [
                    b'bytes',
                  ],
                  'DataType': 'string'
                }
              },
              'MessageSystemAttributes': {
                'string': {
                  'StringValue': 'string',
                  'BinaryValue': b'bytes',
                  'StringListValues': [
                    'string',
                  ],
                  'BinaryListValues': [
                    b'bytes',
                  ],
                  'DataType': 'string'
                }
              },
              'MessageDeduplicationId': 'string',
              'MessageGroupId': 'string',
              'JMSMessageType': 'byte' | 'text',
              'JMSCorrelationId': 'string',
              'JMSReplyTo': {
                'QueueName': 'string',
                'QueueUrl': 'string'
              }
            },
          ]
        )
        ```

        **Response**

        The same as [`send_message_batch`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.send_message_batch)

    
    *   `send_text_message(JMSReplyTo=None, JMSCorrelationId=None, **kwargs)`

        **Request**
        
        The same as [`send_message`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.send_message) with the following additions:

        ```
        response = client.send_text_message(
          JMSReplyTo={
            'QueueName': 'string',
            'QueueUrl': 'string'
          },
          JMSCorrelationId='string',
          ...
        )
        ```

        **Response**

        The same as [`send_message`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.send_message)

*   **`sqs_java_messaging.resource.JMSQueue`**

    ```
    import boto3
    from sqs_java_messaging.resource import JMSQueue

    queue = JMSQueue(boto3.resource('sqs').Queue('url'))
    ```

    This class wraps [`SQS.Queue`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#queue) objects. It provides all of the methods, attributes, identifiers, sub-resources and collections of those objects directly ***except*** `receive_messages`, `send_message` and `send_messages`. These are replaced with `receive_jms_messages`, `send_bytes_message`, `send_text_message` and
    `send_jms_messages`.
    
    Once created it may be used exactly as the wrapped `SQS.Queue` object.

    *   `receive_jms_messages(**kwargs)`

        **Request**

        Exactly as [`receive_messages`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.receive_messages).


        **Response**

        ```
        list(sqs_java_messaging.message.JMSBytesMessage | sqs_java_messaging.message.JMSTextMessage)
        ```


    *   `send_bytes_message(JMSReplyTo=None, JMSCorrelationId=None, **kwargs)`

        **Request**
        
        The same as [`send_message`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.send_message) with the following changes:

        ```
        response = client.send_bytes_message(
          JMSReplyTo={
            'QueueName': 'string',
            'QueueUrl': 'string'
          },
          JMSCorrelationId='string',
          MessageBody=b'bytes' | bytearry,
          ...
        )
        ```

        **Response**

        The same as [`send_message`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.send_message)

    *   `send_jms_messages(**kwargs)`

        **Request**

        The same as [`send_messages`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.send_messages) with the additon of `JMSMessageType`, `JMSCorrelationId` and `JMSReplyTo` and a modification of `MessageBody`.

        ```
        response = client.send_jms_messages(
          Entries=[
            {
              'Id': 'string',
              'MessageBody': 'string' | b'bytes' | bytearry,
              'DelaySeconds': 123,
              'MessageAttributes': {
                'string': {
                  'StringValue': 'string',
                  'BinaryValue': b'bytes',
                  'StringListValues': [
                    'string',
                  ],
                  'BinaryListValues': [
                    b'bytes',
                  ],
                  'DataType': 'string'
                }
              },
              'MessageSystemAttributes': {
                'string': {
                  'StringValue': 'string',
                  'BinaryValue': b'bytes',
                  'StringListValues': [
                    'string',
                  ],
                  'BinaryListValues': [
                    b'bytes',
                  ],
                  'DataType': 'string'
                }
              },
              'MessageDeduplicationId': 'string',
              'MessageGroupId': 'string',
              'JMSMessageType': 'byte' | 'text',
              'JMSCorrelationId': 'string',
              'JMSReplyTo': {
                'QueueName': 'string',
                'QueueUrl': 'string'
              }
            },
          ]
        )
        ```

        **Response**

        The same as [`send_messages`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.send_messages)

    
    *   `send_text_message(JMSReplyTo=None, JMSCorrelationId=None, **kwargs)`

        **Request**
        
        The same as [`send_message`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.send_message) with the following additions:

        ```
        response = client.send_text_message(
          JMSReplyTo={
            'QueueName': 'string',
            'QueueUrl': 'string'
          },
          JMSCorrelationId='string',
          ...
        )
        ```

        **Response**

        The same as [`send_message`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.send_message)
    

*   **`sqs_java_messaging.message.JMSBytesMessage`** and **`sqs_java_messaging.message.JMSTextMessage`**

    These classes wrap [`SQS.Message`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#message) objects. They provide all of the methods,attributes, and identifiers of those objects directly. The sub-resource [`Queue()`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Message.Queue) returns a `JMSQueue`.
    
    Once created it may be used exactly as the wrapped `SQS.Message` object.

    These are the resource's additional available attributes:

    * `jms_correlation_id`
    * `jms_message_type`
    * `jms_reply_to` - a `dict` containing the keys `QueueName` and `QueueUrl`
