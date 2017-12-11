import os
import unittest
import tempfile
import sys
sys.path.append('..')
import urllib  # cant use urllib2 in python3 :P
import config
# import sample_strings
from flask import Flask
from flask.ext.testing import TestCase
from server import app

class StartingTestCase(TestCase):
    def setUp(self):
        self.client = app.test_client()
        config.WTF_CSRF_ENABLED = False
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='pags'"""


        # # load sample strings
        # self.small_str = sample_strings.small_text
        # self.medium_str = sample_strings.medium_text
        # self.large_str = sample_strings.large_text

    def tearDown(self):
        pass

    def create_app(self):
        """
        This is a requirement for Flask-Testing
        """
        app = Flask(__name__)
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='pags'"""
        app.config['TESTING'] = True
        self.baseURL = "http://localhost:5000"
        return app

    # --------------------------------------------------------------------------
    # Simple tests to make sure server is UP
    # The Application MUST be running on the baseURL addr
    # for this test to pass
    # --------------------------------------------------------------------------
    def test_real_server_is_up_and_running(self):
        response = urllib.request.urlopen(self.baseURL)
        self.assertEqual(response.code, 200)
        # returned source code is stored in
        # response.read()

# --------------------------------------------------------------------------
    # Testing Views with GET
    # --------------------------------------------------------------------------
    def test_view_form_home_get(self):
        rv = self.client.get('/')
        assert rv.status_code == 200
        assert 'Detailed Search' in str(rv.data)

    def test_view_form_detSearch_get(self):
        rv = self.client.get('/det_search')
        assert rv.status_code == 200
        assert 'Select a Genre' in str(rv.data)

    # --------------------------------------------------------------------------
    # Testing Views with POST
    # --------------------------------------------------------------------------
    def test_view_form_search_post(self):
        post_data = {'keyword': 'age of'}
        rv = self.client.post('/search', data=post_data, follow_redirects=True)
        assert rv.status_code == 200
        assert 'Age of Empires' in str(rv.data)

    def test_view_form_login_post(self):
        post_data = {'uname': 'turgut', 'psw': '123'}
        rv = self.client.post('/login', data=post_data, follow_redirects=True)
        # assert rv.status_code == 302
        assert 'turgut@itu.edu.tr' in str(rv.data)




    # def test_view_form_resumo_post_with_textrank(self):
    #     post_data = {'texto': self.small_str, 'algorithm': 'textrank'}
    #     rv = self.client.post('/', data=post_data, follow_redirects=True)
    #     assert rv.status_code == 200
    #     assert 'Todos os direitos reservados' in str(rv.data)


    # def test_ajax_resumo_post(self):
    #     post_data = {'texto': self.small_str}
    #     rv = self.client.post('/ajax_resumo',
    #                           data=post_data,
    #                           follow_redirects=True)
    #     assert rv.status_code == 200
    #     # the ajax view returns nothing but the string
    #     assert b'Todos os direitos reservados' == rv.data


    # def test_ajax_resumo_post_with_textrank(self):
    #     post_data = {'texto': self.small_str, 'algorithm': 'textrank'}
    #     rv = self.client.post('/ajax_resumo',
    #                           data=post_data,
    #                           follow_redirects=True)
    #     assert rv.status_code == 200
    #     assert b'Todos os direitos reservados' == rv.data


if __name__ == '__main__':
    unittest.main()