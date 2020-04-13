"""
Test for core module api added here
"""
import json

from rest_framework.test import APITestCase

from authentication.models import Role, User
from core.models import EventType, Event


class RestAPITest(APITestCase):
    """
    Test cases are created in this class
    """

    def setUp(cls):
        """
        Data set up for the unit test
        :return:
        """
        role = Role(role="organizer")
        role.save()
        content = {
            "email": "usertest@mail.com",
            "name": "usertest@mail.com",
            "password": "user123",
            "contact": "9999911111",
            "address": "Bangalore",
            "role": "organizer",
            "organization": "Eventhigh"
        }

        cls.client.post('/authentication/registration', json.dumps(content),
                        content_type='application/json')

        data = dict(email="usertest@mail.com", password="user123")
        login_response = cls.client.post('/authentication/login', json.dumps(data),
                                         content_type='application/json')
        cls.user_id = login_response.data['data']['user']['user_id']
        cls.token = login_response.data['data']['access']
        cls.user = User.objects.get(id=cls.user_id)

        event_type = EventType(type="test")
        event_type.save()

        cls.event = Event(name="test_event", type=event_type, description="New Event",
                          date="2020-04-02",
                          time="12:38:00", location="karnal", subscription_fee=499,
                          no_of_tickets=250,
                          images="https://www.google.com/images", sold_tickets=2,
                          external_links="google.com",
                          event_created_by_id=cls.user_id)
        cls.event.save()

    def test_send_mail_to_a_friend_post_api_with_valid_data(self):
        """
        Unit test for send email to friends  post Api
        :return:
        """
        # Setup

        json_data = {
            "email_id": "",
            "message": "test message"
        }

        # Run
        response = self.client.post("/core/share-with-friend/", json.dumps(json_data),
                                    HTTP_AUTHORIZATION="Bearer {}".format(self.token),
                                    content_type="application/json")

        #  Check
        self.assertEqual(response.status_code, 200)

    def test_subscriber_notify_post_api_with_invalid_data(self):
        """
        Unit test for notify post api
        :return:
        """
        # Setup
        json_data = {
            "event_id": 1,
            "message": "test message",
            "type": "reminder"
        }

        # Run
        response = self.client.post("/core/notify-subscriber/", json_data,
                                    HTTP_AUTHORIZATION="Bearer {}".format(self.token),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
