import yaml
from locust import events

def api_data():
  with open("./data/apidata.yaml", encoding="UTF-8", errors="ignore") as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)
  return data


def write_str_file(str,file_name='1.txt'):
	with open("./report/"+file_name,"a+") as foo:
		foo.write(str)
	return file_name


def events_request(status,eventType="",name="", recvText="", total_time=0,e=''):
    if status == "success":
        events.request_success.fire(request_type=eventType,
                                    name=name,
                                    response_time=total_time,
                                    response_length=len(recvText))
    if status == "failed":
        events.request_failure.fire(request_type=eventType,
                                    name=name,
                                    response_time=total_time,
                                    response_length=len(recvText),
                                    exception=e)
