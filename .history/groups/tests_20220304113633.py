from django.test import TestCase
from users.models import CustomUser
from django.urls import reverse
from django.contrib import auth
from django.test.client import Client
from notes.models import Topic
from notes.tests import createTopic
from groups.forms import MyGroupForm, NewMemberForm

from .models import MyGroup
from .views import group



def createUser(username, password):

    return CustomUser.objects.create_user(username=username, password=password)


def createGroup(name, admin):
    return MyGroup.objects.create(name=name, admin=admin)

class GroupsViewTest(TestCase):
    def setUp(self):
        self.user = createUser('foo', 'foo123')
        self.client.login(username='foo', password='foo123')

    def test_group_is_visible(self):

        group = createGroup(name='test_group',admin=self.user)
        group.user_set.add(self.user)
        
        response = self.client.get(reverse('groups:groups'))
        self.assertEquals(response.status_code,200)
        return self.assertQuerysetEqual(response.context['groups'], [group])
    
    def test_no_group(self):

        response = self.client.get(reverse('groups:groups'))

        self.assertContains(response, "Aktualnie nie masz żadnej grupy.")
        self.assertQuerysetEqual(response.context['groups'], [])

    def test_two_groups_are_visible(self):
        
        group = createGroup(name='test_group',admin=self.user)
        group1 = createGroup(name='test_group1',admin=self.user)
        group.user_set.add(self.user)
        group1.user_set.add(self.user)

        response = self.client.get(reverse('groups:groups'))

        self.assertEquals(response.status_code,200)
        return self.assertQuerysetEqual(response.context['groups'], [group, group1], ordered=False)

    def test_two_groups_each_for_diffrent_user(self):

        user = createUser('foo1','foo123')
        group = createGroup(name='test_group',admin=user)
        group1 = createGroup(name='test_group1',admin=self.user)
        group.user_set.add(user)
        group1.user_set.add(self.user)
        response = self.client.get(reverse('groups:groups'))
        self.assertQuerysetEqual(response.context['groups'],[group1])
    
    def test_new_group_link_is_displayed(self):

        response = self.client.get(reverse('groups:groups'))
        self.assertContains(response, '<a href="%s">Utwórz nową grupe</a>' % reverse('groups:new_group'),
                                 html=True )
    


class NewGroupViewFormTest(TestCase):

    def setUp(self):
        self.user = createUser('foo', 'foo123')
        self.client.login(username='foo', password='foo123')
        self.group = createGroup('test', admin=self.user)
        self.group.user_set.add(self.user)
    
    def test_content_of_site(self):

        response = self.client.get(reverse('groups:new_group'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/new_group.html')
        self.assertContains(response, "Utwórz nową grupe")
    
    def test_creating_new_group(self):

        form = MyGroupForm(self.user, data={"name": "test1"})
        self.assertTrue(form.is_valid())

        new_group = form.save(commit=False)
        new_group.admin = self.user
        new_group.save()
        new_group.user_set.add(self.user)

        response = self.client.get(reverse('groups:groups'))
        self.assertQuerysetEqual(response.context['groups'],[self.group, new_group], ordered=False)

    def test_creating_group_with_existing_name(self):

        form = MyGroupForm(self.user,data={"name": "test"})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('name', code="group_same_name"))
    
    def test_empty_form(self):

        form = MyGroupForm(self.user,data={"name": ""})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('name'))
    

class GroupViewTest(TestCase):

    def setUp(self):
        self.user = createUser('foo', 'foo123')
        self.client.login(username='foo', password='foo123')
        self.group = createGroup('test', admin=self.user)
        self.group.user_set.add(self.user)
    
    def test_content_of_site(self):
        
        response = self.client.get(reverse("groups:group", 
                    kwargs={"group_id": self.group.id}))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/group.html')
    
        self.assertContains(response, '<a href="%s"><h2>%s</h2></a>' %
                             (reverse('groups:groups'),self.group.name), html=True )
    
        self.assertContains(response,'<a href="%s">Dodaj nowy temat</a>' %
                             reverse('notes:group_new_topic', kwargs={"group_id":self.group.id})
                             , html=True )
        self.assertNotContains(response,'<a href="%s">Usuń z grupy</a>' %
                             reverse('groups:delete_from_group', kwargs={"group_id":self.group.id})
                             , html=True )
        self.assertContains(response,'<a href="%s">Dodaj do grupy</a>' %
                             reverse('groups:add_to_group', kwargs={"group_id":self.group.id})
                             , html=True )
        self.assertContains(response,'<a href="%s">Usuń grupe</a>' %
                             reverse('groups:delete_group', kwargs={"group_id":self.group.id})
                             , html=True )

        self.assertQuerysetEqual(response.context['topics'], [])
        self.assertQuerysetEqual(response.context['group'].user_set.all(),
                                 [self.user])

    def test_two_users_in_group(self):

        user = createUser("foo1", "foo123")
        self.group.user_set.add(user)

        response = self.client.get(reverse("groups:group", 
                    kwargs={"group_id": self.group.id}))

        self.assertQuerysetEqual(response.context['group'].user_set.all(),
                                 [self.user, user], ordered=False)

    
    def test_is_topic_is_visible(self):

        topic = createTopic("test2",self.user,access="grp", group=self.group)
   
        response = self.client.get(reverse("groups:group", 
                    kwargs={"group_id": self.group.id}))
        
        self.assertQuerysetEqual(response.context['topics'], [topic])


    def test_two_topics_are_visible(self):

        topic = createTopic("test2",self.user,access="grp", group=self.group)
        topic1 = createTopic("test1",self.user,access="grp", group=self.group)

        response = self.client.get(reverse("groups:group", 
                    kwargs={"group_id": self.group.id}))
        
        self.assertQuerysetEqual(response.context['topics'], [topic, topic1], ordered=False)

    def test_topic_is_no_visible(self):

        response = self.client.get(reverse("groups:group", 
                    kwargs={"group_id": self.group.id}))
        
        self.assertQuerysetEqual(response.context['topics'], [])
        self.assertContains(response,"Nie został jeszcze dodany żaden temat")

    def test_delete_user(self):

        user = createUser('test1','test123')
        self.group.user_set.add(user)
        response = self.client.get(reverse("groups:group",
                    kwargs={"group_id": self.group.id}))
        
        self.assertContains(response,'<a href="%s">Usuń z grupy</a>' %
                             reverse('groups:delete_from_group', kwargs={"group_id":self.group.id})
                             , html=True )
        self.assertQuerysetEqual(response.context['group'].user_set.all(),
                                 [self.user, user], ordered=False)
        
        self.group.user_set.remove(user)
        response = self.client.get(reverse("groups:group",
                    kwargs={"group_id": self.group.id}))
        self.assertNotContains(response,'<a href="%s">Usuń z grupy</a>' %
                             reverse('groups:delete_from_group', kwargs={"group_id":self.group.id})
                             , html=True )
        self.assertQuerysetEqual(response.context['group'].user_set.all(),
                                 [self.user], ordered=False)
    
    def test_delete_group(self):

        response = self.client.get(reverse("groups:group",
                    kwargs={"group_id": self.group.id}))
        
        self.assertEquals(response.status_code, 200)
        self.group.delete()
        response = self.client.get(reverse("groups:group",
                    kwargs={"group_id": self.group.id}))
        self.assertEquals(response.status_code, 404)
        response = self.client.get(reverse("groups:groups"))
        self.assertQuerysetEqual(self.user.groups.all(),[])
        self.assertQuerysetEqual(response.context['groups'],[])

    def test_if_topics_is_deleted_with_group(self):

        topic = createTopic("test2",self.user,access="grp", group=self.group)
        response = self.client.get(reverse("groups:group",
                    kwargs={"group_id": self.group.id}))

        self.assertQuerysetEqual(response.context['topics'], [topic])
        self.assertEquals(response.status_code, 200)
        self.group.delete()
        response = self.client.get(reverse("groups:group",
                    kwargs={"group_id": self.group.id}))
        self.assertFalse(Topic.objects.filter(id=topic.id).exists())
        self.assertEquals(response.status_code, 404)
        response = self.client.get(reverse("groups:groups"))
        self.assertQuerysetEqual(response.context['groups'],[])

class AddToGroupFormTest(TestCase):

    def setUp(self):
        self.user = createUser('foo', 'foo123')
        self.client.login(username='foo', password='foo123')
        self.group = createGroup('test', admin=self.user)
        self.group.user_set.add(self.user)
    

    def test_add_new_member(self):

        user = createUser("test","foo123")
        form = NewMemberForm(self.group,data={"username":"test"})
        self.assertTrue(form.is_valid())
        user1 =  CustomUser.objects.filter(username=form.cleaned_data['username'])
        self.group.user_set.add(user1.get().id)
        response = self.client.get(reverse("groups:group",
                    kwargs={"group_id": self.group.id}))
        self.assertQuerysetEqual(response.context['group'].user_set.all(),
                                 [self.user, user], ordered=False)
    def test_add_existing_member(self):

        user = createUser("test","foo123")
        self.group.user_set.add(user)
        form = NewMemberForm(self.group,data={"username":"test"})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("username", code="user_exists_in_group"))

    def test_adding_unexisting_user(self):
        form = NewMemberForm(self.group,data={"username":"test"})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("username", code="user_does_not_exist"))


class DeleteFromGroupTest(TestCase):

    def setUp(self):
        self.user = createUser('foo', 'foo123')
        self.client.login(username='foo', password='foo123')
        self.group = createGroup('test', admin=self.user)
        self.group.user_set.add(self.user)
    
    def test_no_members_besides_admin(self):

        response = self.client.get(reverse("groups:group",
                    kwargs={"group_id": self.group.id}))
        self.assertNotContains(response,'<a href="%s">Usuń z grupy</a>' %
                             reverse('groups:delete_from_group', kwargs={"group_id":self.group.id})
                             , html=True )
    def test_delete_member(self):

        user = createUser("test","foo123")
        self.group.user_set.add(user)
        response = self.client.get(reverse("groups:group",
                    kwargs={"group_id": self.group.id}))
        self.assertContains(response,'<a href="%s">Usuń z grupy</a>' %
                             reverse('groups:delete_from_group', kwargs={"group_id":self.group.id})
                             , html=True )
        response = self.client.get(reverse("groups:delete_from_group",
                    kwargs={"group_id": self.group.id}))
        
        self.assertQuerysetEqual(response.context['group'].user_set.exclude(username=self.user),
                                [user], ordered=False)   
        self.assertContains(response,'<a style="font-size: 13px;" href="%s">Usuń</a>' %
                             reverse('groups:delete_user', kwargs={"group_id":self.group.id,
                             "user_id":user.id}), html=True )
        
        self.group.user_set.remove(user)
        response = self.client.get(reverse("groups:group",
                    kwargs={"group_id": self.group.id}))
        
        self.assertQuerysetEqual(response.context['group'].user_set.all(),
                                [self.user], ordered=False)   


    