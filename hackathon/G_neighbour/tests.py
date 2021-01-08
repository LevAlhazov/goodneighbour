from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from django.utils import timezone

from .views import *
from .models import donation_card, request_card
from .forms import DonationCardForm, CreateUserForm


# ------------------------------------------------------------------------------------------------------------------------------------------------------
# testing views

class SimpleTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_home(self):
        request = self.factory.get('')
        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_ban(self):
        request = self.factory.get('/banned/')
        response = ban(request)
        self.assertEqual(response.status_code, 200)

    def test_generaldonations(self):
        request = self.factory.get('/generaldonations/')
        response = generaldonations(request)
        self.assertEqual(response.status_code, 200)

    def test_mymessagest(self):
        request = self.client.get('/mymessages/')
        self.assertTemplateUsed(request, 'mymessages.html')

    def test_sentmessages(self):
        request = self.client.get('/sentmessages/')
        self.assertTemplateUsed(request, 'sentmessages.html')

    def test_information(self):
        request = self.client.get('/informationpage/')
        self.assertTemplateUsed(request, 'informationpage.html')

    def test_emergencypage(self):
        request = self.client.get('/emergencypage/')
        self.assertTemplateUsed(request, 'emergencypage.html')
    # -------------user needed here....----------------------------------#

    def test_viewdonation(self):
        request = self.factory.get('/donations/')
        request.user = AnonymousUser()
        response = donations(request)
        self.assertNotEqual(response.status_code, 404)

    def test_viewcompleted(self):
        request = self.factory.get('/completeddonations/')
        request.user = AnonymousUser()
        response = donations(request)
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        request = self.factory.get('/login/')
        request.user = AnonymousUser()
        response = loginuser(request)
        self.assertNotEqual(response.status_code, 404)

    def test_signup(self):
        request = self.factory.get('/signup/')
        request.user = AnonymousUser()
        response = signupuser(request)
        self.assertEqual(response.status_code, 200)

    def test_signout(self):
        request = self.factory.get('/logout/')
        request.user = AnonymousUser()
        request.method = 'Get'
        response = logoutuser(request)
        self.assertEqual(response.status_code, 302)

    def test_create(self):
        request = self.factory.get('/create/')
        request.user = AnonymousUser()
        request.method = 'Get'
        response = createdonationcard(request)
        self.assertEqual(response.status_code, 302)

    def test_userprofile(self):
        request = self.factory.get('/userprofile/')
        request.user = AnonymousUser()
        response = userprofile(request)
        self.assertEqual(response.status_code, 200)

# # ------------------------------------------------------------------------------------------------------------------------------------------------------
#testing model
class donation_and_request_cars_models(TestCase):
    def setUp(self):
        return donation_card.objects.create(title="test", content="this is test",created=timezone.now(),datecompleted=timezone.now())

    def test_donationcard(self):
        w = self.setUp()
        self.assertTrue(isinstance(w, donation_card))

    def test_requestcard(self):
        x = self.setUp()
        self.assertFalse(isinstance(x, request_card))

    def test_location_model(self):
        x = self.setUp()
        self.assertFalse(isinstance(x, request_card))

class information_page_model(TestCase):
    def setUp(self):
        return information_page.objects.create(title="test", content="this is test")

    def test_information_page(self):
        x = self.setUp()
        self.assertTrue(x, request_card)

# # ------------------------------------------------------------------------------------------------------------------------------------------------------
# testing forms
class donation_card_form(TestCase):
    def test_valid_form_donation_card(self):
        w = donation_card.objects.create(title="test", content="this is test")
        data = {'title': w.title, 'content': w.content, }
        form = DonationCardForm(data=data)
        self.assertTrue(form.is_valid()!=True)

class RateForm_form(TestCase):
    def test_valid_RateForm_form(self):
        w = user_rating.objects.create(rating="5", comment="this is test")
        data = {'rating': w.rating, 'comment': w.comment, }
        form = RateForm(data=data)
        self.assertTrue(form.is_valid(),True)

class emergency_page_form(TestCase):
    def test_emergency_page_form(self):
        w = emergency_page.objects.create(name="test", email="test@test.com",number="Test Number")
        data = {'name': w.name, 'email': w.email,'number':w.number}
        form = EmergencyPage(data=data)
        self.assertTrue(form.is_valid(),True)
