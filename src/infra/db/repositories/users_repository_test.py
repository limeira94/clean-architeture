import pytest
from sqlalchemy import text
from src.infra.db.settings.connection import DBConnectionHandler
from .users_repository import UsersRepository


db_connection_handler = DBConnectionHandler()
connection = db_connection_handler.get_engine().connect()

@pytest.mark.skip(reason='Sensive test')
def test_insert_user():
    mocked_first_name = 'first'
    mockerd_last_name = 'last'
    mocked_age = 54
    
    users_repository = UsersRepository()
    users_repository.insert_user(
        first_name=mocked_first_name,
        last_name=mockerd_last_name,
        age=mocked_age
    )
    
    sql = f'''
        SELECT * FROM users
        WHERE first_name = '{mocked_first_name}'
        AND last_name = '{mockerd_last_name}'
        AND age = '{mocked_age}'
    '''
    
    response = connection.execute(text(sql))
    registry = response.fetchall()[0]
    
    assert registry.first_name == mocked_first_name
    assert registry.last_name == mockerd_last_name
    assert registry.age == mocked_age
    
    connection.execute(text(f'DELETE FROM users WHERE id = {registry.id}'))
    connection.commit()


@pytest.mark.skip(reason='Sensive test')
def test_select_user():
    mocked_first_name = 'first_2'
    mockerd_last_name = 'last_2'
    mocked_age = 54
    
    sql = f'''
        INSERT INTO users (first_name, last_name, age)
        VALUES ('{mocked_first_name}', '{mockerd_last_name}', '{mocked_age}')
    '''
    connection.execute(text(sql))
    connection.commit()
    
    users_repository = UsersRepository()
    response = users_repository.select_user(mocked_first_name)

    assert response[0].first_name == mocked_first_name
    assert response[0].last_name == mockerd_last_name
    assert response[0].age == 54    
    
    connection.execute(text(f'DELETE FROM users WHERE id = {response[0].id}'))
    connection.commit()