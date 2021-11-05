from django.test import TestCase

# Create your tests here.
from selenium import webdriver
from .forms import HashForm
import hashlib
from .models import Hash
from django.core.exceptions import ValidationError
import time

#below lines are for functional test.

class FunctionalTest(TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def testHomepage(self):
		self.browser.get('http://localhost:8000')
		self.assertIn('Enter Hash Here:', self.browser.page_source)

	def testHashExist(self):
		self.browser.get('http://localhost:8000')
		text = self.browser.find_element_by_id('id_text')
		text.send_keys('Hello')
		self.browser.find_element_by_name('submit').click()
		self.assertIn('185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969', self.browser.page_source)

	def test_ajax_hash(self):
		self.browser.get('http://localhost:8000')
		text = self.browser.find_element_by_id('id_text')
		text.send_keys('Hello')
		time.sleep(5) #to wait for 5 seconds
		self.assertIn('185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969', self.browser.page_source)

	def tearDown(self):
		self.browser.quit()

#below lines are for unit test

class UnitTest(TestCase):

	def test_homepage_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

	def test_hash_form(self):
		form = HashForm(data={'text':'hello'})
		self.assertTrue(form.is_valid())

	def test_hash_works(self):
		hash_text = hashlib.sha256(b'Hello').hexdigest()
		self.assertEqual('185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969', hash_text)

	def saveHash(self):
		hash = Hash()
		hash.text = 'Hello'
		hash.hash = "185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969"
		hash.save()
		return hash

	def test_hash_object(self):
		hash = self.saveHash()
		pulled_hash = Hash.objects.get(text = 'Hello')
		self.assertEqual(pulled_hash.hash, '185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969')

	def test_viewing_hash(self):
		hash = self.saveHash()
		response = self.client.get('/hash/185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969')
		self.assertContains(response, 'Hello')

	def test_bad_hash(self):
		def badHash():
			hash = Hash()
			hash.hash = "185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969hfguijka"
			hash.full_clean()
		self.assertRaises(ValidationError, badHash)




