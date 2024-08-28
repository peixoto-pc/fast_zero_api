from http import HTTPStatus

from fast_zero_api.models import TodoState
from tests.conftest import TodoFactory


def test_create_todo(client, token):
    response = client.post(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )

    assert response.json() == {
        'id': 1,
        'title': 'Test todo',
        'description': 'Test todo description',
        'state': 'draft',
    }


def test_list_5_todos(session, client, user, token):
    expect_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get('/todos/', headers={'Authorization': f'Bearer {token}'})

    assert len(response.json()['todos']) == expect_todos


def test_list_todos_pagination_2_todos(session, user, token, client):
    expect_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == expect_todos


def test_list_todos_filter_title_5_todos(session, user, token, client):
    expect_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, title='Test todo title')
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test todo title', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == expect_todos


def test_list_todos_filter_description_5_todos(session, user, token, client):
    expect_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, description='Test todo description')
    )
    session.commit()

    response = client.get(
        '/todos/?description=Test todo description',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expect_todos


def test_list_todos_filter_state_5_todos(session, user, token, client):
    expect_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft)
    )
    session.commit()

    response = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expect_todos


def test_delete_todo(session, user, token, client):
    # cria um todo novo
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    # delete do todo criado
    response = client.delete(
        f'/todos/delete/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfully.'}


def test_delete_todo_not_found(token, client):
    # delete de todo errado
    response = client.delete(
        '/todos/delete/-1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_update_todo(session, user, token, client):
    # cria um novo todo
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.patch(
        f'/todos/update/{todo.id}',
        json={'title': 'Teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'Teste!'


def test_update_todo_not_found(token, client):
    # update de todo errado
    response = client.patch(
        '/todos/update/-1',
        json={'title': 'Teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}
