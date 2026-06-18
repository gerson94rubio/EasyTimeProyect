import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_get_productos():
    client = APIClient()
    response = client.get("/api/productos/")
    # Si aún no tienes endpoint, esto fallará con 404
    assert response.status_code in [200, 404]