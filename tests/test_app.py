from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'Cuca',
            'email': 'cuca@fdp.com',
            'password': 'soufdp',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Cuca',
        'email': 'cuca@fdp.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
