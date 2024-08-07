from http import HTTPStatus

from jwt import decode

from fast_zero_api.security import create_access_token
from fast_zero_api.settings import Settings

settings = Settings()


def test_jwt():
    data_payload = {'sub': 'test@test.com'}
    token = create_access_token(data_payload)
    result = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert result['sub'] == data_payload['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer token-invalido'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
