# Work in progress to establish baseline infrastructure and plumbing for python edge modules
# Needs extreme cleanup

import random
import time
import sys
import os
import datetime
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# choose HTTP, AMQP or MQTT as transport protocol
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
AVG_WIND_SPEED = 10.0
MSG_TXT = "{\"deviceId\": \"MyFirstPythonDevice\",\"windSpeed\": %.2f}"

def iothub_client_init(connStr):

    # prepare iothub client
    client = IoTHubClient(connStr, PROTOCOL)

    # set the time until a message times out
    client.set_option("messageTimeout", MESSAGE_TIMEOUT)
    
    CERT_FILE = os.environ['EdgeModuleCACertificateFile']        
    print("Adding TrustedCerts from: {0}".format(CERT_FILE))
    
    # this brings in x509 privateKey and certificate
    file = open(CERT_FILE)
    try:
        client.set_option("TrustedCerts", file.read())
        print("Added cert")
    except IoTHubClientError as iothub_client_error:
        print('Setting IoT Edge TrustedCerts failed (%s)' % iothub_client_error)
    
    file.close()

    return client

def send_confirmation_callback(message, result, user_context):

    map_properties = message.properties()
    print ( "    message_id: %s" % message.message_id )
    print ( "    correlation_id: %s" % message.correlation_id )

    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )


def init(connStr):

    try:
        client = iothub_client_init(connStr)

        while True:

            msg_txt_formatted = MSG_TXT % (
                AVG_WIND_SPEED + (random.random() * 4 + 2))

            # messages can be encoded as string or bytearray
            message = IoTHubMessage(msg_txt_formatted)
            client.send_event_async("temperatureOutput", message, send_confirmation_callback, None)

            # Wait for Commands or exit
            print ( "IoTHubClient waiting for commands, press Ctrl-C to exit" )

            status = client.get_send_status()
            print ( "Send status: %s" % status )
            time.sleep(10)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':

    print ( "\nPython %s" % sys.version )

    try:
        CONNECTION_STRING = os.environ['EdgeHubConnectionString']
        print(CONNECTION_STRING)

    except Exception as option_error:

        print ( option_error )
        sys.exit(1)

    print ( "Starting the IoT Hub Python sample..." )
    print ( "    Connection string=%s" % CONNECTION_STRING )

    init(CONNECTION_STRING)