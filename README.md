RubyPipe
========

RubyPipe allows you to pipe selected text in Sublime Text 2 or 3 through Ruby.

To run the command open the command palette and search for Ruby. The two choices
are: "Pipe Selection with Ruby" and "Pipe Selection with Ruby (Replace)". Both
will perform similar actions but the latter will replace the selected text with
the ouput of the Ruby command.

For example consider the following text:

    This is a test and I want to know how many words have more than three characters.

Select the text and than run "Pipe Selection with Ruby" and enter the following
Ruby code in the input panel.

    $_.split(" ").select{|w| w.size > 3 }.size

After executing this will bring up a message box showing: 11. Other
possibilities for this plugin are to use Ruby to quickly reformat text by using
ruby to process the input.

In your Ruby script the content of the selection is available in all of the
following variables: `$_`, `$select`, or `$text`. 