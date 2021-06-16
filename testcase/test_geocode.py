import pytest
from utils.help import api_data

class TestGeocode:
	def test_geo(self,req):
		url = api_data()["geocode_geo"]["api"]+"address="+api_data()["geocode_geo"]["address"]+"&key="+api_data()['key']

		response = req.get(url)
		assert response.status_code == 200

	def test_regeo(self,req):
		url = api_data()["geocode_regeo"]["api"]+"location="+api_data()["geocode_regeo"]["location"]+"&key="+api_data()['key']

		response = req.get(url)
		assert response.status_code == 200