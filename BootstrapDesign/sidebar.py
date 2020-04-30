import pandas as pd
from django.conf import settings


class Url:
	
	def __init__(self, link, param=0):
		""" Support only one parameter"""
		self.link = link
		self.param = param


class Menus(object):
	"""
	Manage menus according to the user profile
	--> active : active page to highlight in the menu
	--> is_anonymous : personalise menu according to the log in statut
	"""
	
	def __init__(self, active, request,
		menuTexts = settings.SIDEBAR_MENU_TEXTS, menuUrls = settings.SIDEBAR_MENU_URLS,
		manageAccount=True):
		super(Menus, self).__init__()
		self.active = active
		self.menus, self.menu_urls = [], []
		self.menu_icons = ['home', 'menu_book']
		self.menus.extend(menuTexts)
		self.menu_urls.extend(menuUrls)

		if manageAccount:
			if request.user.is_anonymous:
				self.menus.append("Log in")
				self.menu_urls.append('login')
				self.menu_icons.append('account_circle')
			else:
				self.menus.extend(['Account'])
				self.menu_urls.extend([Url('accounts')])
				self.menu_icons.extend(['account_circle'])

				#Convert the string to Urls
		for i,l in enumerate(self.menu_urls):
			if type(l)==type('a'):
				self.menu_urls[i] = Url(l)

		self.i = 0

	def __iter__(self):
		return self

	def __next__(self):
		i=self.i
		if i >= len(self.menus):
			raise StopIteration
		self.i+=1
		return self.Menu(
			self.menus[i], 
			self.menu_urls[i],
			self.is_active(i),
			self.menu_icons[i])

	def is_active(self, n):
		if n==self.active:
			return "active"
		else:
			return ''

	class Menu:
		"""docstring for Menu"""
		def __init__(self, title, menu_url, active, icon):
			self.title = title
			self.menu_url = menu_url
			self.active = active
			self.icon = icon