"""
test.py

This is not really well developed yet, ideally I would move this to the unittest framework.

This test script currently doesn't do a bunch - it is only checking that the curl command will give a "response recieved", and that an e-mail file is generated for it.

Launch server, and then this script.

"""

import subprocess
import message_types
import time

api_command = 'curl -X POST -H \'Content-type: application/json\' --data  \'{"start_time":"08/27/2019 21:04", "end_time":"08/27/2019 22:04",   "program_id":1, "event_type":"market_dispatch"}\' http://localhost:8080/'
api_command_bad = 'curl -X POST -H \'Content-type: application/json\' --data  \'{"start_time":"08/27/2019 21:04", "end_time":"08/27/2019 22:04",   "program_id":1, "event_type":"fake_event"}\' http://localhost:8080/'

# I'm using shell=true command for the scope of this project, but wouldn't use in a production environment due to safety concerns.


def test_response_ok():
    proc = subprocess.Popen(
        api_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = proc.communicate()
    time.sleep(1)  # giving a second to avoid a race condition with writing the files
    print("testing if user response generated...")
    assert (
        stdout.decode("utf8") == "Request recieved\n"
    ), "test_response_ok: Response was not recieved by client"


def test_email_generated():
    proc = subprocess.Popen(
        api_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )

    stdout, stderr = proc.communicate()
    time.sleep(1)  # giving a second to avoid a race condition with writing the files
    with open("emails.txt", "r") as fp:
        print("testing if e-mail generated...")
        assert (
            "Dear Voltan" in fp.read()
        ), "test_email_generated: email file was not written"


def test_error_logged():
    proc = subprocess.Popen(
        api_command_bad, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = proc.communicate()
    time.sleep(1)  # giving a second to avoid a race condition with writing the files
    print("testing if correct error generated...")
    with open("error_logger_log.txt", "r") as fp:
        assert (
            message_types.ERROR_UNSUPPORTED_EVENT in fp.read()
        ), "test_error_logged: invalid event was not logged properly"


test_response_ok()
test_email_generated()
test_error_logged()
