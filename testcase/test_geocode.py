import pytest
from conftest import api_data,key

class TestGeocode:
	def test_geo(self,req):
		url = api_data["geocode_geo"]["api"]+"address="+api_data["geocode_geo"]["address"]+"&key="+key

		response = req.get(url)
		assert response.status_code == 200

	def test_regeo(self,req):
		url = api_data["geocode_regeo"]["api"]+"location="+api_data["geocode_regeo"]["location"]+"&key="+key

		response = req.get(url)
		assert response.status_code == 200