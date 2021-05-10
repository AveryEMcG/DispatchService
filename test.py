import subprocess

api_command = "curl -X POST -H 'Content-type: application/json' --data  '{\"start_time\":\"08/27/2019 21:04\", \"end_time\":\"08/27/2019 22:04\",   \"program_id\":1, \"event_type\":\"market_dispatch\"}\' http://localhost:8080/"


def test_response_ok():
    proc = subprocess.Popen(cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
 

test_response_ok()


# curl -X POST -H 'Content-type: application/json' --data   '{"start_time":"08/27/2019 21:04", "end_time":"08/27/2019 22:04",   "program_id":1, "event_type":"market_dispatch"}' http://localhost:8080/ 
