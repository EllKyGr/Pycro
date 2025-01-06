# Pycro
A tailored Micro Editor for <ins>Python development</ins>

This are a set of several files, tips and recommendations using Micro while
developing in Python.

### Syntax
Micro currently can highlight more than 100 languages and users can customize
their editor with several methods. Although the repository counts with several
[syntax files](https://github.com/zyedidia/micro/tree/master/runtime/syntax), and it's stated how can be improved to better suit the user
experience, at the present it only addresses basic statements and keywords.
Thus the expanded syntax file present here adds type hint, function calls and
several other new handy highlighted cases.
This isn't by any means a full fledged error prove file: either by current
Micro limitations, statement overruling, missing regex statements (or isn't
specific enough) some words might not be highlighted as expected (i.e urls).
Add to `~/.config/micro/syntax/` the `python3.yaml` after installing Micro.

### Color schemes
Present color schemes are designed to comply with the syntax file. Custom
color schemes should follow the same rules in order to work properly. Both
files contain commentary enough explaining which command is responsible for
the specific color scheme.
For instance *pyrcula.micro* expands/modifies the original color scheme from
*darcula.micro* to adjust for the new statements.
Add to `~/.config/micro/colorschemes/` the `color_scheme_file.micro` either from
here, the Micro [repo](https://github.com/zyedidia/micro/tree/master/runtime/colorschemes) or a custom one.

### Sample
Several simple lines of code which encompasses the most common highlighted
cases for fast checking or test.

Although the present files are specific for Python, the overall code template present in here for
both syntax and color scheme can be adjusted to meet the specifics of any other language. Refer to the Micro syntax
repository if the language is already supported and modify it as desired.

## How to set
1. Installing Micro:
	Micro 2.0.XX => https://github.com/benweissmann/getmic.ro
2. Plugins `micro -plugin install <plugin>`:
	- [`aspell`](https://github.com/priner/micro-aspell-plugin): spell checking. `addpersonal` adds word to personal dict when cursor is placed under said word.

	- [`filemanager`](https://github.com/NicolaiSoeborg/filemanager-plugin): adds a tree to visualize, open, create files and directories:
	    - `Ctrl + e` then `tree`: open the file tree
	    - `left key` or `right key`: closes or collapses the directory
	    - `rename`: new name for selected file inside tree
        - `rm`: deletes file inside tree
	    - `touch`: creates file in the current path
	    - `mkdir`: creates directory in current path

	- [`lsp`](https://github.com/AndCake/micro-plugin-lsp): adds language server for better coding style and formatting
		- Run `pip install python-lsp-server` for the lsp plugin to work
		- `Alt + d`: with cursor under a function returns the documentation
		- `Alt + k`: with cursor under function, object, etc returns brief description at status line
		- `Ctrl + _`: comments out the line. Repeat to undo previous action
		- `Ctrl + space`: limited auto complete; all possible keywords are listed yet not cleanly stated

	- `autofmt`: formats file content at save based on language. Until the new
	   [autofmt](https://github.com/a11ce/micro-autofmt) repo is updated with a `-plugin` command, do this instead:
		1. `git clone git@github.com:a11ce/micro-autofmt.git`
		2. `cd` to micro-autofmt/ then `make`. The cloned repository is no longer needed after installing the plugin files so it can be removed aftewards.
		3. Currently only C/C++/C#, Python, Racket, JavaScript, Rust and Go are supported.
			   Every language require its specific formatter
		4. For Python run: `pip install` git+https://github.com/google/yapf.git
			   either directly or within environment.
	- [`runit`](https://github.com/terokarvinen/micro-run): allows to run, compile and make files on the go.
		- `F5`: saves and run
		- `F12`: makes
		- `F5`: makes in the background

	- [`manipulator`](https://github.com/NicolaiSoeborg/manipulator-plugin): add commands inside Micro for alternative edition i.e. `Ctrl + e` followed by:
		- `dquote` wraps selected text within double quotes
		- `curly` wraps selected text within {}
		- `camel` turns text into camelCase format  


      __NOTE:__ Refer to the main page of the repository, or the *manipulator.md* after installed, to learn all the available commands. The plugin installs version __1.4.0__, version __1.4.1__ is needed for `camel, snake, kebab`, etc to work otherwise Micro won't recognize them.
	- [`quoter`](https://github.com/sparques/micro-quoter): wraps the lines with double or single quotes.
	- [`cheat`](https://github.com/terokarvinen/micro-cheat): pressing `F1` opens a new tab with a cheatsheet of concepts from the current working language. Although mostly basic concepts of the language, the file can be modify and expand upon as needed.  
 	 __NOTE:__ the path stated in *main.lua* at line 11 __=>__ *local cheatdir = config.ConfigDir.."/plug/micro-cheat/cheatsheets/"*
	           conflicts with the actual path installed for the plugin, instead of __micro-cheat__ change it to __cheat__


3. Settings and key bindings:
	after installing plugins edit, or create, the `settings.json` at `~/.config/micro`
	with the following options:
    ```
    # settings.json
	{
	    "aspell.check": "on",
	    "aspell.lang": "en",       # Native or any language
	    "colorcolumn": 80,         # Rule
	    "colorscheme": "pyrcula",  # Or any color scheme fitting the python syntax file
	    "diffgutter": true,        # Visual cue for changes in current file
	    "fmt-onsave": true,        # Format on save
	    "hlsearch": true,          # Matched letters and background color
	    "hltrailingws": true,      # Any type of white space is highlighted
	    "savecursor": true,        # Cursor locates in its last position from previous session
	    "scrollbar": true          # Optional

	    # lsp plugin will update file with the following options

	    "lsp.ignoreMessages": "LS message1 to ignore|LS message 2 to ignore|...",
	    "lsp.ignoreTriggerCharacters": "completion,signature",
	    "lsp.server": "python=pylsp",

	}
	```
	Enter `Ctrl + e` inside Micro and then `set` followed by any additional option you may want in addition to the recommended ones.

	Check the Micro [options](https://github.com/zyedidia/micro/blob/master/runtime/help/options.md) tab for further information

	```
	# Expected bindings to be found in `bindings.json` after plugin install
	{
	    "Alt-/": "lua:comment.comment",
	    "Alt-d": "command:definition",
	    "Alt-f": "command:format",
	    "Alt-k": "command:hover",
	    "Alt-r": "command:references",
	    "CtrlSpace": "command:lspcompletion",
	    "CtrlUnderscore": "lua:comment.comment",
	    "F1": "command:cheat",
	    "F12": "command:makeup",
	    "F5": "command:runit",
	    "F9": "command:makeupbg"
	}
	```

	Check the Micro [keybindings](https://github.com/zyedidia/micro/blob/master/runtime/help/keybindings.md) tab for further information
