from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Tree(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	slug = models.SlugField(null=False)

	class Meta:
		constraints = [models.UniqueConstraint(fields= ['user','slug'], name="user-tree-unique"),]

	def __str__(self):
		return self.user.username + " | " + self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Tree, self).save(*args, **kwargs)

class Link(models.Model):
	tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
	name = models.CharField(max_length=30, null=False)
	url = models.URLField()

	def __str__(self):
		return self.url