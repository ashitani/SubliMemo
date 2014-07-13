# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import os
import fnmatch
import datetime
import time

class SubliMemoBase:
	def __init__(self):
		self.settings=sublime.load_settings("SubliMemo.sublime-settings")
		settings = self.settings
		self.path = self.settings.get("path")
		self.extension = self.settings.get("extension")

		if ((self.path == None) or (self.path=="")):
			print("can't load settings")
			self.path_error()
			return
		self.path=os.path.normpath(self.path)
		try:
			self.file_list = os.listdir(self.path)
			self.file_list = fnmatch.filter(self.file_list,'*.'+self.extension)
		except FileNotFoundError:
			print("*."+self.extension+" not found")
			self.path_error()
			return
		self.file_list.sort()
		self.file_list.reverse()

	def path_error(self):
		sublime.error_message("Prease set path preferly.\n(Preferences-Package Settings-SubliMemo)")


class CreateSubliMemoCommand(sublime_plugin.TextCommand, SubliMemoBase):

	def __init__(self,args):
		SubliMemoBase.__init__(self)
		sublime_plugin.TextCommand.__init__(self,args)

	def on_done(self,word):
		date = datetime.datetime.today().strftime("%Y%m%d")		
		datet = datetime.datetime.today().strftime("%Y/%m/%d")		
	
		filename = self.path + "/" + date + "_" + word + "." + self.extension
		v = self.view.window().open_file(filename)

		def set_text():
			if v.is_loading():
				sublime.set_timeout_async(set_text, 0.1)
			else:
				v.run_command("insert_my_text",{"args":{'text':"# "+datet+" "+word+"\n\n"}})
		set_text()

	def run(self,edit):
		self.edit=edit
		self.view.window().show_input_panel("Memo Name:", 
			"", self.on_done, None,None)


class InsertMyText(sublime_plugin.TextCommand):
  def run(self, edit, args):
  	v=self.view
  	v.insert(edit, 0, args['text'])

class FindSubliMemoCommand(sublime_plugin.WindowCommand, SubliMemoBase):

	def __init__(self,args):
		SubliMemoBase.__init__(self)
		sublime_plugin.WindowCommand.__init__(self,args)

	def run(self):
		project = self.window.project_data()
		if ((project == {} ) or (project==None)):
			project= {'folders': [{'path': self.path}]}
		else:
			project['folders'].append({'path': self.path})

		self.window.set_project_data(project)
		self.window.run_command("show_panel", {"panel": "find_in_files","args": {} } )

class SubliMemoListner(sublime_plugin.EventListener, SubliMemoBase):

	def __init__(self):
		sublime_plugin.EventListener.__init__(self)

	def post_text_command(self,view, command_name, args):
		sublime.error_message(command_name)

	def on_pre_close(self,view):
		if (view.name()=="Find Results"):
			SubliMemoBase.__init__(self)
			try:
				project = view.window().project_data()
				f=project['folders']
			except:
				return
			f_new=[]
			for item in f:
				if(item['path']==self.path):
					pass
				else:
					f_new.append(item)
			
			if(f_new==[]):
				view.window().set_project_data({})
			else:
				project['folders']=f_new
				view.window().set_project_data(project)

