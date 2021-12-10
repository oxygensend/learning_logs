from django.db.models.query import QuerySet
from django.test import TestCase
from django.urls import reverse
from .models import Topic, User, Entry
from .forms import TopicForm, EntryForm, TopicAccessForm
# Create your tests here.



def createTopic(topic, user, access=True):
    """ Create new Topic """
    return Topic.objects.create(text=topic, owner = user, access=access)

def createEntry(entry, topic, creator):
    """ Create new Entry """
    return Entry.objects.create(text=entry, topic=topic, creator=creator)


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
        self.assertQuerysetEqual(response.context['topics_public'], [])
        return self.assertQuerysetEqual(response.context['topics_private'], [])

    def test_access__if_user_no_logged_in(self):
        """If user is not logged in login panel should display"""

        response = self.client.post(reverse('learning_logs:topics'))

        return  self.assertEqual(response.status_code, 302)


    def test_adding_new_private_topic(self):
        """ Test wether adding goes wrong"""

        self.client.login(username='foo', password='foo123')
        new_topic = createTopic(topic="fooo", user=self.user)
        response = self.client.post(reverse('learning_logs:topics'))
        return self.assertQuerysetEqual(response.context['topics_private'], [new_topic])

    def test_adding_new_public_topic_user_is_owner(self):
        """ Test adding new public topic (should be displayed in topics_private if user is owner)"""

        self.client.login(username='foo', password='foo123')
        new_topic = createTopic(topic="fooo", user=self.user, access=False)
        response = self.client.post(reverse('learning_logs:topics'))  
        return self.assertQuerysetEqual(response.context['topics_private'], [new_topic])



    def test_adding_one_public_one_private_topic_user_is_owner(self):
        """ Adding two topics public and private"""
        self.client.login(username='foo', password='foo123')

        new_topic1 = createTopic(topic="fooo", user=self.user, access=False)
        new_topic = createTopic(topic="fooo2", user=self.user, access=True)
        response = self.client.post(reverse('learning_logs:topics'))
        return self.assertQuerysetEqual(response.context['topics_private'], [new_topic1, new_topic])

    def test_adding_new_public_topic_user_is_not_owner(self):
        """ Test adding new public topic (should be displayed in topics_private if user is owner)"""

        self.client.login(username='foo', password='foo123')
        user = createUser('foo1', 'foo123')

        new_topic = createTopic(topic="fooo", user=user, access=False)
        response = self.client.post(reverse('learning_logs:topics'))  
        return self.assertQuerysetEqual(response.context['topics_public'], [new_topic])

   
class TopicViewTest(TestCase):
    """ Tests for Topic View """
    def setUp(self):
        self.user = createUser('foo', 'foo123')

    def test_access_if_user_no_logged(self):
        """If user is not logged in login panel should display"""

        topic = createTopic('foo', self.user)
        response = self.client.post(reverse('learning_logs:topic' ,kwargs={'topic_id':topic.id}))
        return  self.assertEqual(response.status_code, 302)

    def test_change_access(self):
        """ Test if changing access work properly"""

        topic = createTopic('foo', self.user, True)
        self.client.login(username='foo', password='foo123')
        form = TopicAccessForm(instance=topic,data={'access': False})
        self.assertTrue(form.is_valid())
        form.save()
        return self.assertEquals(topic.access, False)

    def test_delete_topic(self):
        """ Test if topic delete properly"""

        topic = createTopic('foo', self.user, True)
        self.client.login(username='foo', password='foo123')
    
        response = self.client.post(reverse('learning_logs:topics' ))
        self.assertQuerysetEqual(response.context['topics_private'], [topic])
        topic.delete()
        response = self.client.post(reverse('learning_logs:topics' ))

        return self.assertQuerysetEqual(response.context['topics_private'], [])

    def test_delete_not_your_topic(self):
        """ Test if u can delete not ur topic"""
        
        user = createUser('test','test123')
        self.client.login(username='test', password='test123')
        topic = createTopic('foo', self.user, False)
        response = self.client.post(reverse('learning_logs:delete_topic', kwargs={'topic_id':topic.id}))
        return self.assertEquals(response.status_code, 404)

    def test_firstly_edit_your_entry_secondly_edit_not_your_entry(self):
        """ Test """

        user = createUser('test','test123')
        topic = createTopic('foo', self.user, True)
        entry1 = createEntry('test1',topic,self.user)
        entry2 = createEntry('test2',topic, user)

        self.client.login(username='foo', password='foo123')
        response = self.client.post(reverse('learning_logs:edit_entry', 
                                            kwargs={'entry_id': entry1.id}))
        self.assertEquals(response.status_code, 200)
        response = self.client.post(reverse('learning_logs:edit_entry', 
                                            kwargs={'entry_id': entry2.id}))
        return self.assertEquals(response.status_code, 404)




class NewTopicFormTest(TestCase):
    """ Test for Topic Form"""
    def setUp(self):
        self.user = createUser('foo', 'foo123')
        self.client.login(username='foo', password='foo123')
    

    def test_same_name_topic(self):
        """ If topic with same name exists with the same access display proper message"""

        new_topic = createTopic(topic="fooo", user=self.user)        
        form = TopicForm(self.user, data={'text': 'fooo', 'access':True})
        self.assertFalse(form.is_valid())
        
        return self.assertTrue(form.has_error('text',code="topic_exists"))
    
    def test_access_error_topic(self):
        """ If access for topic is not selected display proper message """
        form = TopicForm(self.user, data={'text': 'fooo'})
        self.assertFalse(form.is_valid())
        return self.assertTrue(form.has_error('access'))
    
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
        response = self.client.get('')
        entry = createEntry('test entry 123', self.topic, response.wsgi_request.user)
        response = self.client.post(reverse('learning_logs:topic', 
                            kwargs={'topic_id': self.topic.id}))
        return self.assertQuerysetEqual(response.context['entries'], [entry])    
    
    def test_add_two_entries(self):
        """ Adding two new entries"""

        response = self.client.get('')
        entry1 = createEntry('test entry 1', self.topic, response.wsgi_request.user)
        entry2 = createEntry('test entry 2', self.topic, response.wsgi_request.user)

        response = self.client.post(reverse('learning_logs:topic', 
                            kwargs={'topic_id': self.topic.id}))
        return self.assertQuerysetEqual(response.context['entries'], 
                            [entry2, entry1])               
    
    def test_edit_entry(self):
        """ Edit entry """

        response = self.client.get('')
        entry = createEntry('test entry 1', self.topic, response.wsgi_request.user)
        form = EntryForm(self.topic,instance=entry, data={'text': 'test entry 1 edit'})
        form.save()
        response = self.client.post(reverse('learning_logs:topic',
                            kwargs={'topic_id': self.topic.id}))
        return self.assertQuerysetEqual(response.context['entries'],
                            [entry])
    
    def test_delete_entry(self):
        """ Delete entry """

        entry = createEntry('test entry 1', self.topic, self.user)    
        entry.delete()
    
        response = self.client.post(reverse('learning_logs:topic',
                            kwargs={'topic_id': self.topic.id}))
        return self.assertQuerysetEqual(response.context['entries'],
                            [])



