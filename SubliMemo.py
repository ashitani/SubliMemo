# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import os
import fnmatch
import datetime

class SubliMemoBase:
	def __init__(self):
		self.settings=sublime.load_settings("SubliMemo.sublime-settings")
		settings = self.settings
		self.path = self.settings.get("path")

		if ((self.path == None) or (self.path=="")):
			self.path = ""
			sublime.error_message("Prease set path preferly\n(Preferences-Package Settings-SubliMemo)")
			return
		self.path+="/"
		try:
			self.file_list = os.listdir(self.path)
			self.file_list = fnmatch.filter(self.file_list,'*.txt')
		except FileNotFoundError:
			sublime.error_message("Prease set path preferly.\n(Preferences-Package Settings-SubliMemo)")
			return
		self.file_list.sort()
		self.file_list.reverse()

class CreateSubliMemoCommand(sublime_plugin.TextCommand, SubliMemoBase):
	
	def __init__(self,args):
		self.args=args
		SubliMemoBase.__init__(self)
		sublime_plugin.TextCommand.__init__(self,args)

	def on_done(self,word):
		date = datetime.datetime.today().strftime("%Y%m%d_")		
		filename = self.path + date + word + ".txt"
		v = self.view.window().open_file(filename)

	def run(self,edit):
		self.view.window().show_input_panel("Memo Name:", 
			"", self.on_done, None,None)

class GotoSubliMemoCommand(sublime_plugin.WindowCommand, SubliMemoBase):

	def __init__(self,args):
		self.args=args
		SubliMemoBase.__init__(self)
		sublime_plugin.WindowCommand.__init(self,args)

	def on_select(self, idx):
		if idx < 0:
			return
		pass
		self.window.open_file(self.path+self.file_list[idx])

	def run(self):
		sublime.active_window().show_quick_panel(self.file_list, self.on_select)
