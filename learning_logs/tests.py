from django.db.models.query import QuerySet
from django.test import TestCase
from django.urls import reverse
from .models import Topic, User, Entry
from .forms import TopicForm, EntryForm
# Create your tests here.



def createTopic(topic, user):
    """ Create new Topic """
    return Topic.objects.create(text=topic, owner = user)

def createEntry(entry, topic):
    """ Create new Entry """
    return Entry.objects.create(text=entry, topic=topic)


def createUser(username, password):
    """ Create new user """
    return User.objects.create_user(username=username, password=password)

class TopicsViewTest(TestCase):
    """ Tests for topics view function"""
    def setUp(self):
        self.user = createUser('foo', 'foo123')

    def test_no_topic(self):
        """If no topic exists appropriate message displays"""
        
        self.client.login(username='foo', password='foo123')
        response = self.client.post(reverse('learning_logs:topics'))

        self.assertContains(response, "Nie został jeszcze dodany żaden temat.")

        return self.assertQuerysetEqual(response.context['topics'], [])

    def test_access__if_user_no_logged_in(self):
        """If user is not logged in login panel should display"""

        response = self.client.post(reverse('learning_logs:topics'))
        print(response.context)
        return  self.assertEqual(response.status_code, 302)


    def test_adding_new_topic(self):
        """ Test wether adding goes wrong"""

        self.client.login(username='foo', password='foo123')
        new_topic = createTopic(topic="fooo", user=self.user)
        response = self.client.post(reverse('learning_logs:topics'))
        return self.assertQuerysetEqual(response.context['topics'], [new_topic])



class NewTopicFormTest(TestCase):
    """ Test for Topic Form"""
    def setUp(self):
        self.user = createUser('foo', 'foo123')
        self.client.login(username='foo', password='foo123')
    

    def test_same_name_topic(self):
        """ If topic with same name exists display proper message"""

        new_topic = createTopic(topic="fooo", user=self.user)        
        form = TopicForm(self.user, data={'text': 'fooo'})
        self.assertFalse(form.is_valid())
        return self.assertTrue(form.has_error('text',code="topic_exists"))
    
    def test_same_name_diffrent_case_size_topic(self):
        """ If topic with same name but with different size case exists display proper message"""

        new_topic = createTopic(topic="fooo", user=self.user)        
        form = TopicForm(self.user, data={'text': 'FooO'})
        self.assertFalse(form.is_valid())
        return self.assertTrue(form.has_error('text',code="topic_exists"))
    
    def test_if_field_is_empty(self):
        """ If topic field is empty form shouldnt be send"""

        form = TopicForm(self.user, data={'text': ''})
        self.assertFalse(form.is_valid())
        return self.assertTrue(form.has_error('text'))


class EntryFormTests(TestCase):
    """ Tests for entry form """

    def setUp(self):
        self.user = createUser('foo', 'foo123')
        self.topic = createTopic('foo', self.user)
        self.client.login(username='foo', password='foo123')

    def test_add_new_entry(self):
        """ Adding new entry to topic"""

        entry = createEntry('test entry 123', self.topic)
        response = self.client.post(reverse('learning_logs:topic', 
                            kwargs={'topic_id': self.topic.id}))
        return self.assertQuerysetEqual(response.context['entries'], [entry])    
    
    def test_add_two_entries(self):
        """ Adding two new entries"""
        entry1 = createEntry('test entry 1', self.topic)
        entry2 = createEntry('test entry 2', self.topic)

        response = self.client.post(reverse('learning_logs:topic', 
                            kwargs={'topic_id': self.topic.id}))
        return self.assertQuerysetEqual(response.context['entries'], 
                            [entry2, entry1])               
    
    def test_edit_entry(self):
        """ Edit entry """

        entry = createEntry('test entry 1', self.topic)
        form = EntryForm(self.topic,instance=entry, data={'text': 'test entry 1 edit'})
        form.save()
        response = self.client.post(reverse('learning_logs:topic',
                            kwargs={'topic_id': self.topic.id}))
        return self.assertQuerysetEqual(response.context['entries'],
                            [entry])
    
    # def test_delete_entry(self):
    #     """ Delete entry """

    #     entry = createEntry('test entry 1', self.topic)    
    #     entry.delete()
        
    #     response = self.client.post(reverse('learning_logs:topic',
    #                         kwargs={'topic_id': self.topic.id}))
    #     return self.assertQuerysetEqual(response.context['entries'],
    #                         [])
    