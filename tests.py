import os
import unittest
import tempfile
import sys
sys.path.append('..')
import urllib
import config
from flask import Flask
from flask.ext.testing import TestCase
from server import app

class StartingTestCase(TestCase):
    def setUp(self):
        self.client = app.test_client()
        config.WTF_CSRF_ENABLED = False
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='pags'"""
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

    def test_real_server_is_up_and_running(self): # RUNNING CHECK
        response = urllib.request.urlopen(self.baseURL)
        self.assertEqual(response.code, 200)

    def test_view_form_a_home_get(self): # HOME
        rv = self.client.get('/')
        assert rv.status_code == 200
        assert 'Detailed Search' in str(rv.data)

    def test_view_form_b_login_post(self): # LOGIN - POST
        post_data = {'uname': 'turgut', 'psw': '123'}
        rv = self.client.post('/login', data=post_data, follow_redirects=True)
        #assert rv.status_code == 302
        assert 'turgut@itu.edu.tr' in str(rv.data)

    def test_view_form_c_initdb_get(self): # INITDB - POST
        self.test_view_form_b_login_post()
        rv = self.client.get('/initdb')
        assert 'Redirecting' or 'Detailed Search' in str(rv.data)

    def test_view_form_d_detSearch_get(self): # DETAILED SEARCH - ASSERT CHECK
        rv = self.client.get('/det_search')
        assert rv.status_code == 200
        assert 'Select a Genre' in str(rv.data)

    def test_view_form_e_gameprofile_get(self): # GAME PROFILE PAGE CHECK
        rv = self.client.get('/gameprofile/343') # BF3
        assert 'Battlefield 3' in str(rv.data)

    def test_view_form_f_search_post(self): # SEARCH - POST
        post_data = {'keyword': 'age of'}
        rv = self.client.post('/search', data=post_data, follow_redirects=True)
        assert rv.status_code == 200
        assert 'Age of Empires' in str(rv.data)

    def test_view_form_g_detsearch_post(self): # DETAILED SEARCH - POST
        post_data = {'keyword': 'battlefield', 'genre':'5','category':'DLC/Addon','rating':'80'}
        rv = self.client.post('/send_detsearch', data=post_data, follow_redirects=True)
        assert 'Battlefield 2: Euro Force' in str(rv.data)

    def test_view_form_h_logout_get(self): # LOGOUT
        self.test_view_form_b_login_post()
        rv = self.client.get('/logout', follow_redirects=True)
        assert 'Logged Out' in str(rv.data)

    def test_view_form_i_recommend_without_hw_post(self): # RECOMMEND RESULTS - WITHOUT HARDWARE
        self.test_view_form_b_login_post()
        post_data = {'game1': 'battlefield', 'game2': 'call of duty', 'game3': 'sniper elite 3'}
        rv = self.client.post('/engine',data=post_data, follow_redirects=True)
        assert 'Wolfenstein' in str(rv.data)

    def test_view_form_j_confighw_get(self): # CONFIG HARDWARE - GET
        self.test_view_form_b_login_post()
        rv = self.client.get('/confighw')
        assert rv.status_code == 200
        assert 'Select a CPU' in str(rv.data)

    def test_view_form_k_confighw_post(self): # SAVE HW - POST
        self.test_view_form_b_login_post()
        post_data = {'cpu': 'AMD Athlon 7750', 'gpu': 'AMD HD 5770','ram': '4 GB', 'os': 'Windows'}
        rv = self.client.post('/savehw', data=post_data, follow_redirects=True)
        rv = self.client.get('/profile', follow_redirects=True)
        assert 'AMD Athlon 7750' in str(rv.data)

    def test_view_form_l_recommend_get(self): # RECOMMEND PAGE
        self.test_view_form_b_login_post()
        rv = self.client.get('/pags', follow_redirects=True)
        assert 'Recommend Me Games!' in str(rv.data)

    def test_view_form_m_recommend_with_hw_post(self): # RECOMMEND RESULTS WITH HARDWARE
        self.test_view_form_b_login_post()
        self.test_view_form_k_confighw_post()
        post_data = {'game1': 'battlefield', 'game2': 'call of duty', 'game3': 'sniper elite 3'}
        rv = self.client.post('/engine',data=post_data, follow_redirects=True)
        assert 'Age of Empires' in str(rv.data)
        assert 'Wolfenstein' not in str(rv.data)

    def test_view_form_n_gameprofile_with_hw_get(self): # GAME PROFILE SYSTEM REQ CONTROL
        self.test_view_form_b_login_post()
        self.test_view_form_k_confighw_post()
        rv = self.client.get('/gameprofile/343') # BF3 SHOULD NOT RUN
        assert 'frown' in str(rv.data)
        assert 'Battlefield' in str(rv.data)
        rv = self.client.get('/gameprofile/289') # AOE SHOULD RUN
        assert 'smile' in str(rv.data)
        assert 'Age of' in str(rv.data)
        rv = self.client.get('/gameprofile/8575') # UNKNOWN SPECS
        assert 'question' in str(rv.data)
        assert 'Castle' in str(rv.data)

if __name__ == '__main__':
    unittest.main()
