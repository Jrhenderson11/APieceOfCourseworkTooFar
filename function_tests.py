from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()
from django.contrib.auth.models import User

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless()
        self.browser = webdriver.Firefox(firefox_options=fireFoxOptions)

        # add test user to users
        #User.objects.get(username='test_user').delete()
        try:
            user = User.objects.create_superuser('test_user', 'temporary@website.com', 'test_password')
        except:
            pass


    def tearDown(self):
        try:
            User.objects.get(username='test_user').delete()
        except:
            pass
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Visit website
        self.browser.get('http://localhost:8000')

        # Check title
        self.assertIn('Blogs', self.browser.title)

        # Notices link to CV page, follows it
        self.assertIn('CV', [x.text for x in self.browser.find_elements_by_xpath('//a')])
        self.browser.find_element_by_link_text("CV").click()
        
        # reads CV
        self.assertIn('Skills', [x.text for x in self.browser.find_elements_by_xpath('//h3')])

        # Logs in as admin
        self.browser.find_element_by_link_text("Admin").click()
        inputbox = self.browser.find_element_by_name('username')
        inputbox.send_keys('test_user')
        inputbox = self.browser.find_element_by_name('password')
        inputbox.send_keys('test_password')
        self.browser.find_element_by_xpath("//form/div[3]/input").click()


        # Edits CV
        self.browser.get('http://localhost:8000/cv')
        self.browser.find_element_by_css_selector("a.btn.btn-default").click()


        inputbox = self.browser.find_element_by_name("skills")
        inputbox.send_keys('new skills')
        inputbox = self.browser.find_element_by_name("education")
        inputbox.send_keys('new education')
        self.browser.find_element_by_css_selector("button.save.btn.btn-default").click()

        # Checks edits have worked correctly
        self.assertIn('new skills', self.browser.find_elements_by_class_name('inner')[1].text)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
