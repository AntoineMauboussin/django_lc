from django.test import TestCase,Client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.urls import reverse
import time
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class SeleniumTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_insert_item(self):
        self.selenium.get(f"{self.live_server_url}/accounts/register")
        #driver.get("http://127.0.0.1:8000/accounts/login/")

        #connexion en tant qu'utilisateur Linus
        self.selenium.find_element(By.CSS_SELECTOR, '#id_username').send_keys("myuser")
        self.selenium.find_element(By.CSS_SELECTOR, '#id_password1').send_keys("secret")
        password = self.selenium.find_element(By.CSS_SELECTOR, '#id_password2')
        password.send_keys("secret")
        password.send_keys(Keys.RETURN)
        time.sleep(2)

        user = User.objects.filter(username="myuser")
        assert(user.exists())