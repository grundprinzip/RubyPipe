import sublime
import sublime_plugin
import subprocess

class Stack:

	MAX_SIZE = 2

	def __init__(self):
		self.data = []

	def push(self, x):
		if (len(self.data) == 0 or self.data[0] != x):
			self.data.insert(0, x)

		if(len(self.data) > Stack.MAX_SIZE):
			self.data.pop()

	def top(self):
		if (len(self.data) == 0):
			return ""

		return self.data[0]


call_history = Stack()


class RubyUpdateSelection(sublime_plugin.TextCommand):
	def run(self, edit, sel, data):
		sel = sublime.Region(sel[0], sel[1])
		self.view.replace(edit, sel, data)

class RubyExecBaseCommand(sublime_plugin.TextCommand):

	CODE = """
# be smart, dont print something if we already have..
$write_count = 0
$code = ARGV[0]
$text = ARGV.size > 1 ? ARGV[1] : nil
$select = $text
$_ = $text

def STDOUT.write(what)
   $write_count += 1
   super(what)
end

# execure the code
begin
  # insert a space if input was a selection, if it was a line insert \n
  print($text ? " " : "\n")
  r = eval($code)
rescue Object
  r = $!.class.to_s
end

# try to_s, if it doesnt work use inspect
# Array and Hash are shown via inspect because they look better with formating
# do this just if the script did not print anything itself
if $write_count == 1
  print( (r.class != Hash and r.class != Array and not r.nil? and r.respond_to? :to_s) ? r.to_s : r.inspect )
  print( "\n" ) unless $text.size > 0
end
	"""


	def run(self, edit):

		sel = self.view.sel()
		if (len(sel) != 1):
			sublime.status_message("Only single selections supported!")
			return

	
		self.data = self.view.substr(sel[0])
		self.sel = sel[0]

		last_item = call_history.top()
		sublime.active_window().show_input_panel("Code",last_item,self.on_done, None, None)

	def do_call(self, text):
		call_history.push(text)
		result = subprocess.Popen(["ruby", "-e", RubyExecBaseCommand.CODE, text, self.data], stdout=subprocess.PIPE)
		return result.stdout.read().decode("UTF-8")


class RubyExecSelectionCommand(RubyExecBaseCommand):
	
	def on_done(self, text):
		data = self.do_call(text)
		sublime.message_dialog(data)


class RubyExecSelectionReplaceCommand(RubyExecBaseCommand):
	
	def on_done(self, text):
		data = self.do_call(text)
		sublime.active_window().run_command("ruby_update_selection", {"sel": [self.sel.begin(), self.sel.end()], "data": data})		