from http import HTTPStatus

from fast_zero_api.schema import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_read_html(client):
    response = client.get('/html')
    assert response.status_code == HTTPStatus.OK
    assert response.text.find('Olá Mundo') > 0


def test_create_user(client):
    response = client.post(  # Action
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED  # Assert
    assert response.json() == {  # Assert
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_name_already_exists(client, user):
    response = client.post(  # Action
        '/users/',
        json={
            'username': 'Teste',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST  # Assert
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_already_exists(client, user):
    response = client.post(  # Action
        '/users/',
        json={
            'username': 'Peixoto',
            'email': 'teste@test.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST  # Assert
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Teste',
        'email': 'teste@test.com',
        'id': 1,
    }


def test_get_token(client, user):
    response = client.post(
        '/token', data={'username': user.email, 'password': user.clean_password}
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


def test_update_user_not_found(client, token):
    response = client.put(
        '/users/-1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Cuca',
            'email': 'cuca@fdp.com',
            'password': 'soufdp',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client, token):
    response = client.delete('/users/-1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_read_user_not_found(client):
    response = client.get('/users/-1')

    assert response.status_code == HTTPStatus.NOT_FOUND
