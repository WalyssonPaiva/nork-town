import pytest
from _pytest.monkeypatch import MonkeyPatch as non_fixture_monkeypatch

@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv('APP_SETTINGS', 'config.TestingConfig')
    from app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="session", autouse=True)
def seed(monkeysession):
    monkeysession.setenv('APP_SETTINGS', 'config.TestingConfig')
    from app import app
    app.config['TESTING'] = True
    with app.app_context():
        create_tables()
        populate_tables()

@pytest.fixture(scope="session")
def monkeysession(request):
    mpatch = non_fixture_monkeypatch()
    yield mpatch
    mpatch.undo()

def create_tables():
    from ext import db
    from models import Customer, Car
    db.create_all()

def populate_tables():
    from models import Customer, Car, User
    from werkzeug.security import generate_password_hash
    from ext import db
    customers = [ "John Doe", "Jane Doe", "John Smith", "Jane Smith", "John Black", "Jane Black" ]
    for customer in customers:
        db.session.add(Customer(name=customer))
    cars = [ ("blue", "hatch", 1), ("gray", "sedan", 2), ("blue", "hatch", 3), ("yellow", "convertible", 4), ("BLUE", "hatch", 6)]
    for car in cars:
        db.session.add(Car(color=car[0], model=car[1], owner=car[2]))
    db.session.add(User(username="admin", password=generate_password_hash("admin")))
    db.session.commit()
    
@pytest.fixture
def get_jwt_token(client):
    response = client.post('/login', json={"username": "admin", "password": "admin"})
    return response.json['token']

    