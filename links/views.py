from django.shortcuts import render
from .models import Tree, Link 
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.text import slugify

class UserLinks(ListView):
	'''present a user's tree list'''
	model = Tree
	template_name = 'links/my_links.html'
	succes_url = '/'

	def get_context_data(self, *args, **kwargs):
		#get the page user from the url
		context = super(UserLinks, self).get_context_data(*args, **kwargs)
		context['user_page'] = self.kwargs['username']
		return context

	def get_queryset(self, *args, **kwargs):
		try:
			user=User.objects.get(username=self.kwargs['username'])
		except User.DoesNotExist:
			raise Http404("User does not exist")
		return Tree.objects.filter(user=user).order_by('name')


class UserLinksCreateView(UserPassesTestMixin, CreateView):
	'''if the user is on his page add a new tree'''
	raise_exception = True
	def test_func(self):
		return self.request.user.is_authenticated and self.request.user.username == self.kwargs['username']

	model = Tree
	fields = ['name']
	template_name = 'links/add_entry.html'

	def get_success_url(self):
		return reverse_lazy('user_links', kwargs=self.kwargs)

	def form_valid(self, form):
		if Tree.objects.filter(user=self.request.user, slug=slugify(form.cleaned_data['name'])).exists():
			form.add_error('name', 'Invalid name.')
			return super().form_invalid(form)

		form.instance.user = self.request.user
		return super().form_valid(form)


class UserLinksDeleteView(UserPassesTestMixin, DeleteView):
	'''if the user is on his page delete a tree'''
	raise_exception = True
	def test_func(self):
		return self.request.user.is_authenticated and self.request.user.username == self.kwargs['username']

	model = Tree
	template_name = 'links/delete_tree.html'

	def get_object(self, queryset=None):
		return Tree.objects.get(pk=self.request.POST.get('tree_pk'))

	def get_success_url(self):
		return reverse_lazy('user_links', kwargs=self.kwargs)


class TreeLinks(ListView):
	'''present links of a tree'''
	model = Link
	template_name = 'links/list_of_links.html'

	def get_context_data(self, *args, **kwargs):
		#get the slug and the user page from the url
		context = super(TreeLinks, self).get_context_data(*args, **kwargs)
		context['tree_slug'] = self.kwargs['tree_slug']
		context['user_page'] = self.kwargs['username']
		return context

	def get_queryset(self, *args, **kwargs):
		try:
			tree=Tree.objects.get(slug=self.kwargs['tree_slug'])
		except Tree.DoesNotExist:
			raise Http404("Tree does not exist")

		return Link.objects.filter(tree=tree)


class TreeLinksCreateView(UserPassesTestMixin, CreateView):
	'''if the user is on his page add a link'''
	raise_exception = True
	def test_func(self):
		print(self.request.user)
		return self.request.user.is_authenticated and self.request.user.username == self.kwargs['username']

	model = Link
	fields = ['name', 'url']
	template_name = 'links/add_entry.html'

	def form_valid(self, form):
		form.instance.tree = Tree.objects.get(slug = self.kwargs['tree_slug'])
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('tree_links', kwargs={'username':self.kwargs['username'],'tree_slug': self.kwargs['tree_slug']})


class TreeLinksDeleteView(UserPassesTestMixin, DeleteView):
	'''if the user is on his page remove a link'''
	raise_exception = True
	def test_func(self):
		return self.request.user.is_authenticated and self.request.user.username == self.kwargs['username']

	model = Link

	def get_object(self, queryset=None):
		return Link.objects.get(pk=self.request.POST.get('link_pk'))

	def get_success_url(self):
		return reverse_lazy('tree_links', kwargs={'username':self.kwargs['username'],'tree_slug': self.kwargs['tree_slug']})