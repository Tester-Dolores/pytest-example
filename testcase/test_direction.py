import pytest
from utils.help import api_data

class TestDirection:	
	def test_direction_walking(self,req):
		url = api_data()["direction_walking"]["api"]+"origin="+api_data()["direction_walking"]["origin"]\
			+"&key="+api_data()['key']+"&destination="+api_data()["direction_walking"]["destination"]

		response = req.get(url)
		assert response.status_code == 200

	def test_direction_transit(self,req):
		url = api_data()["direction_transit"]["api"]+"origin="+api_data()["direction_transit"]["origin"]\
			+"&key="+api_data()['key']+"&destination="+api_data()["direction_transit"]["destination"]

		response = req.get(url)
		assert response.status_code == 200