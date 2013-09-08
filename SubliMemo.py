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
			pass_error()
			return
		self.path+="/"
		try:
			self.file_list = os.listdir(self.path)
			self.file_list = fnmatch.filter(self.file_list,'*.txt')
		except FileNotFoundError:
			pass_error()
			return
		self.file_list.sort()
		self.file_list.reverse()

	def path_error():
		sublime.error_message("Prease set path preferly.\n(Preferences-Package Settings-SubliMemo)")


class CreateSubliMemoCommand(sublime_plugin.TextCommand, SubliMemoBase):

	def __init__(self,args):
		SubliMemoBase.__init__(self)
		sublime_plugin.TextCommand.__init__(self,args)

	def on_done(self,word):
		date = datetime.datetime.today().strftime("%Y%m%d_")		
		filename = self.path + date + word + ".txt"
		v = self.view.window().open_file(filename)

	def run(self,edit):
		self.view.window().show_input_panel("Memo Name:", 
			"", self.on_done, None,None)

class FindSubliMemoCommand(sublime_plugin.WindowCommand, SubliMemoBase):

	def __init__(self,args):
		SubliMemoBase.__init__(self)
		sublime_plugin.WindowCommand.__init__(self,args)

	def run(self):
		project = self.window.project_data()
		print(project)
		if ((project == {} ) or (project==None)):
			project= {'folders': [{'path': self.path}]}
			self.window.set_project_data(project)
		else:
			project['folders'].append({'path': self.path})

		self.window.run_command("show_panel", {"panel": "find_in_files"} )

