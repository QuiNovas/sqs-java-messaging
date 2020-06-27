import io

from setuptools import setup

setup(
    name='sqs-java-messaging',
    version='0.0.1',
    description='Implements SQS JMS protocol mirroring amazon-sqs-java-messaging-lib',
    author='Joseph Wortmann',
    author_email='jwortmann@quinovas.com',
    url='https://github.com/QuiNovas/sqs-java-messaging',
    license='Apache 2.0',
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=['sqs_java_messaging'],
    package_dir={'sqs_java_messaging': 'src/sqs_java_messaging'},
    install_requires = [],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
    ],
)
