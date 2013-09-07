# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import datetime

class CreateSubliMemoCommand(sublime_plugin.TextCommand):
	
	def on_done(self,word):
		date = datetime.datetime.today().strftime("%Y%m%d_")		
		filename = self.path + date + word + ".txt"
		v = self.view.window().open_file(filename)

	def run(self,edit):
		self.edit = edit

		self.settings = sublime.load_settings("SubliMemo.sublime-settings")
		self.path = self.settings.get("path")
		if self.path == None:
			self.path = ""

		self.view.window().show_input_panel("Memo Name:", 
			"", self.on_done, None,None)
