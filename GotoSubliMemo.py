# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import datetime
import os

class GotoSubliMemoCommand(sublime_plugin.WindowCommand):

	def on_select(self, idx):
		if idx < 0:
			return
		pass
		self.window.open_file(self.path+self.file_list[idx])

	def run(self):
		self.settings=sublime.load_settings("SubliMemo.sublime-settings")
		settings = self.settings
		self.path = self.settings.get("path")
		if self.path == None:
			self.path = ""

		self.file_list = os.listdir(self.path)
		sublime.active_window().show_quick_panel(self.file_list, self.on_select)