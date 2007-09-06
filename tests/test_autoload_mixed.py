from elixir import *

def setup():
    metadata.bind = 'sqlite:///'

def teardown():
    cleanup_all(True)

class TestAutoloadMixed(object):
    def setup(self):
        conn = metadata.bind.connect()
        conn.execute("""CREATE TABLE user
        (user_id INTEGER PRIMARY KEY AUTOINCREMENT)""")
        conn.close()
        
    def test_belongs_to(self):
        class User(Entity):
            using_options(tablename='user', autoload=True)

        class Item(Entity):
            belongs_to('owner', of_kind='User')

        setup_all(True)

        assert Item.table.c['owner_user_id'].foreign_key.column.name == 'user_id'
