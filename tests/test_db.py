from sqlalchemy import select

from fast_zero_api.models import User


def test_create_user(session):
    new_user = User(username='peixoto', password='furacao', email='pei@xoto.com')

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'peixoto'))

    assert user.username == 'peixoto'
