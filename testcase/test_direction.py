import pytest
from conftest import api_data,key

class TestDirection:
	def test_direction_walking(self,req):
		url = api_data["direction_walking"]["api"]+"origin="+api_data["direction_walking"]["origin"]\
			+"&key="+key+"&destination="+api_data["direction_walking"]["destination"]

		response = req.get(url)
		assert response.status_code == 200


	def test_direction_transit(self,req):
		url = api_data["direction_transit"]["api"]+"origin="+api_data["direction_transit"]["origin"]\
			+"&key="+key+"&destination="+api_data["direction_transit"]["destination"]

		response = req.get(url)
		assert response.status_code == 200