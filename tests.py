import unittest
from flask_testing import TestCase
from app import app, db, User, Game


class YourAppTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        db.create_all()
        user = User(username='testuser', email='test@example.com', password='testpassword', role=2)
        db.session.add(user)

        game = Game(name_en='Test Game', name_ru='Тестовая Игра', tags='best', url='http://www.example.com')
        db.session.add(game)

        db.session.commit()

    '''def tearDown(self):
        db.session.remove()
        db.drop_all()'''

    def test_index_route(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('index.html')

    def test_signup_route(self):
        response = self.client.get('/signup')
        self.assert200(response)
        self.assert_template_used('signup.html')

    def test_signup_functionality(self):
        response = self.client.post('/signup', data=dict(
            username='newuser',
            email='newuser@example.com',
            password='newpassword'
        ), follow_redirects=True)
        self.assert200(response)
        self.assert_template_used('signin.html')

    def test_signin_route(self):
        response = self.client.get('/signin')
        self.assert200(response)
        self.assert_template_used('signin.html')

    def test_choose_route(self):
        response = self.client.get('/choose')
        self.assert200(response)
        self.assert_template_used('choose.html')

    def test_goods_route(self):
        response = self.client.get('/goods')
        self.assert200(response)
        self.assert_template_used('goods.html')

    def test_home_route(self):
        response = self.client.get('/home')
        self.assert200(response)
        self.assert_template_used('index.html')

    def test_index1_route(self):
        response = self.client.get('/index')
        self.assert200(response)
        self.assert_template_used('index.html')

    def test_news_route(self):
        response = self.client.get('/news')
        self.assert200(response)
        self.assert_template_used('news.html')

    def test_contact_route(self):
        response = self.client.get('/contact')
        self.assert200(response)
        self.assert_template_used('contact.html')

    def test_thanks_route(self):
        response = self.client.get('/thanks')
        self.assert200(response)
        self.assert_template_used('thanks.html')

    def test_about_route(self):
        response = self.client.get('/about')
        self.assert200(response)
        self.assert_template_used('about.html')

    def test_error_route(self):
        response = self.client.get('/error')
        self.assert200(response)
        self.assert_template_used('error.html')

    def test_trap_route(self):
        response = self.client.get('/trap')
        self.assert200(response)
        self.assert_template_used('trap.html')

    def test_trap_route(self):
        response = self.client.get('/trap')
        self.assert200(response)
        self.assert_template_used('trap.html')

    def test_not_found_route(self):
        response = self.client.get('/not_found')
        self.assert200(response)
        self.assert_template_used('404.html')


if __name__ == '__main__':
    unittest.main()
