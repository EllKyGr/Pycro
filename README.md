# Pycro
A tailored Micro Editor for <ins>Python development</ins>

This are a set of several files, tips and recommendations using Micro while
developing in Python.

### Syntax
Micro currently can highlight more than 100 languages and users can customize
their editor with several methods. Although the repository counts with several
[syntax files](https://github.com/zyedidia/micro/tree/master/runtime/syntax), and it's stated how can be improved to better suit the user
experience, at the present it addresses general group statements and keywords.
Thus the expanded syntax file present here adds type hint, function calls and
several other new handy highlighted cases.
This isn't by any means a full fledged error prove file: either by current
Micro limitations, statement overruling, missing regex statements (or isn't
specific enough) some words might not be highlighted as expected (i.e urls).

### Color schemes
Present color schemes are designed to comply with the syntax file. Custom
color schemes should follow the same rules in order to work properly. Both
files contain commentary enough explaining which command is responsible for
the specific color scheme.
For instance  __darcula.micro__ in this repository extends/modifies the original color scheme
in vanilla Micro to adjust for the new statements.

### Sample
Several simple lines of code which encompasses the most common highlighted
cases for fast checking or test.

Although the present files are specific for Python, the overall code template present in here for
both syntax and color scheme can be adjusted to meet the specifics of any other language. Refer to the Micro syntax
repository if the language is already supported and modify it as desired.

#### Requirements:
- Python 3 installed
- Either conda, venv or any tool for environment setup (recommended)

## How to set
### TL;DR
1. Create a new Python environment and activate it. (optional but recommended)__*__
2. `git clone git@github.com:EllKyGr/Pycro.git` then `make`

	- `make u-pycro` removes all Pycro related files, i.e. all color schemes within this repository and the __python3.yaml__. __NOTE:__ although several color schemes are extended versions
		of default ones, you can still use them through `set` command or added directly to the `settings.json` after deleting the extended version. If a Micro session is open during removal
		process, exit once deleted, then `reload` to use default version, assuming the current colorscheme matches the same file name.
	- `make u-micro` removes all Pycro and Micro related files from your system. __NOTE:__ if your Micro bin is located anywhere but __/usr/bin__
		this command won't be able to delete it.
	- After the setup is complete you can run `make clean` to remove this repository since its content will no longer be necessary. The __makefile__ would be relocated to the parent directory
		so the previous commands are available. If deleted the removal of Pycro (and/ or Micro) should be perform manually. Refer to the step by step section if that's the case.

#### Termux
1. Install git then shasum with `pkg install perl`
2. `git clone git@github.com:EllKyGr/Pycro.git`
3. Open the makefile and change __(-)__
	```
	micro: checksum
		- cd /usr/bin/; echo "\nInstalling Micro at => $$PWD\n"; \
		+ cd /data/data/com.termux/files/usr/bin/; echo "\nInstalling Micro at => $$PWD\n"; \
		- curl https://getmic.ro | sudo bash;
		+ curl https://getmic.ro | bash;
	```
4. Then `make`. The same commands apply to remove Pycro files and Micro however to remove Micro
through `make u-micro`, the following line should be changed:
	```
	u-micro:
		- cd /usr/bin; echo "Attempting to remove Micro from $$PWD"; sudo rm -i micro; \
		+ cd /data/data/com.termux/files/usr/bin; echo "Attempting to remove Micro from $$PWD"; rm -i micro; \
	```
5. Optional: It is possible, during makefile execution, the target `plugins` may issue the error *Failed to query plugin channel*. If that is your case you can either try run it later,
download individually each plugin or run `python get_plugin.py` (or `./get_plugin.py`); the script will download by default the plugins recommend in here. Be sure to previously install
__requests__ before running the script (`pip install requests`). You can run `python get_plugin.py -pl <plug_1> <plug_2> <plug_n>` or `./get_plugin.py -pl <plug_n>` if different or additional
plugins are needed instead. By default the zip files are downloaded in the current script location; move said files to `~/.config/micro/plug` and extract them in there. Alternatively the
flag `-dir` downloads directly the plugin zip file inside Micro's plug directory: `./get_plugin.py -pl <plug_n> -dir`.

#### Micro already installed?
1. Although not necessary for the present settings, be aware of the __micro__ bin file location. (The __makefile__ can only remove Micro entirely if located at */usr/bin*)
2. Create a new Python environment and activate it. (optional but recommended)__*__
3. `git clone git@github.com:EllKyGr/Pycro.git` then `make pycro`

__*__ The main reason for using a Python environment is just for containment sake. On the other hand the plugins related to these packages (LSP and yapf) will not work as intended if the latter
are missing. Meaning to use Micro's full capacity (while developing Python) these two packages should be present.

### Step by Step
1. Installing Micro:
	- Micro 2.0.XX => https://github.com/benweissmann/getmic.ro
	- Add to `~/.config/micro/syntax/` the `python3.yaml` after installing Micro.
	- Add to `~/.config/micro/colorschemes/` the `color_scheme_file.micro` either from here, the Micro [repo](https://github.com/zyedidia/micro/tree/master/runtime/colorschemes) or a custom one.
	- Optional: create a Python environment with your favorite tool before proceeding.

2. Plugins `micro -plugin install <plugin>`:
	- [`aspell`](https://github.com/priner/micro-aspell-plugin): spell checking. `addpersonal` adds word to personal dictionary when cursor is placed under said word.

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

	- `autofmt`: formats file content at save based on language. Until the current
	   [autofmt](https://github.com/a11ce/micro-autofmt) repository is updated with a `-plugin` command, do this instead:
		1. `git clone git@github.com:a11ce/micro-autofmt.git`
		2. `cd` to micro-autofmt/ then `make`. The cloned repository is no longer needed after installing the plugin files so it can be removed aftewards.
		3. Currently only C/C++/C#, Python, Racket, JavaScript, Rust and Go are supported.
			   Every language require its specific formatter
		4. For Python run: `pip install git+https://github.com/google/yapf.git`
			   either directly or within environment.
	- [`runit`](https://github.com/terokarvinen/micro-run): allows to run, compile and make files on the go.
		- `F5`: saves and run
		- `F12`: makes
		- `F5`: makes in the background

	- [`manipulator`](https://github.com/NicolaiSoeborg/manipulator-plugin): add commands inside Micro for alternative edition, i.e. `Ctrl + e` followed by:
		- `dquote` wraps selected text within double quotes
		- `curly` wraps selected text within {}
		- `camel` turns text into camelCase format  


      __NOTE:__ Refer to the main page of the repository, or the *manipulator.md* after installed, to learn all the available commands. The plugin installs version __1.4.0__, version __1.4.1__
                is needed for `camel, snake, kebab`, etc. to work otherwise Micro won't recognize them. `get_plugin.py` cannot reach the latest version because the Micro's main channel is outdated,
                however the present __makefile__ is capable of retrieving the latest `manipulator.lua` with `make plug-fix` be aware the default save directory may vary according to the installation
                method; as instructed in the __makefile__, the plugin installed with `-plugin` command creates *manipulator* directory plainly, whereas through `get_plugin.py`, or direct download, besides
                *manipulator* the name contains the downloaded version, i.e. *manipulator-plugin* or *manipulator-X.X.X*, if that is the case `manipulator.lua` file will be saved at ~/.config/micro/plug
	- [`quoter`](https://github.com/sparques/micro-quoter): wraps the lines with double or single quotes.
	- [`cheat`](https://github.com/terokarvinen/micro-cheat): pressing `F1` opens a new tab with a cheatsheet of concepts from the current working language. Although mostly basic concepts of the language, the file can be modify and expand upon as needed.  
 	 __NOTE:__ the path stated in *main.lua* at line 11 __=>__ *local cheatdir = config.ConfigDir.."/plug/micro-cheat/cheatsheets/"*
	           conflicts with the actual path installed for the plugin, instead of __micro-cheat__ change it to __cheat__. If the plugin was downloaded through Micro's plugin channel, __micro-cheat__ should
	           be changed to __micro-cheat-0.0.X__ the *X* representing the downloaded version.
	- [`snippets`](https://github.com/micro-editor/updated-plugins/tree/master/micro-snippets-plugin): adds vim like snippets capabilities to Micro, i.e. right next `def`:
		- `Alt + s`: inserts the snippet
		- `Alt + w`: toggle between elements from the snippet
		- `Alt + d`: removes snippet
		- `Alt + a`: exists snippet edition mode


3. Settings and key bindings:
	after installing plugins edit, or create, the `settings.json` at `~/.config/micro`
	with the following options (the lines preceded by __#__ are meant to be deleted):
    ```
    # settings.json
	{
	    "aspell.check": "on",
	    "aspell.lang": "en",       # Native or any language
	    "colorcolumn": 80,         # Rule
	    "colorscheme": "darcula",  # Or any color scheme fitting the Python syntax file
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
	Enter `Ctrl + e` inside Micro and then `set` followed by any additional option you may want in addition to the recommended ones.
	```

	Check the Micro [options](https://github.com/zyedidia/micro/blob/master/runtime/help/options.md) tab for further information

	```
	# Expected key bindings in `bindings.json` after plugin install
	{
        "Alt-/": "lua:comment.comment",
        "Alt-a": "lua:snippets.Accept",
        "Alt-c": "lua:snippets.Cancel",
        "Alt-d": "command:definition",
        "Alt-f": "command:format",
        "Alt-k": "command:hover",
        "Alt-r": "command:references",
        "Alt-s": "lua:snippets.Insert",
        "Alt-w": "lua:snippets.Next",
        "CtrlSpace": "command:lspcompletion",
        "CtrlUnderscore": "lua:comment.comment",
        "F1": "command:cheat",
        "F12": "command:makeup",
        "F5": "command:runit",
        "F9": "command:makeupbg"
	}
	```

	Any keybindings present here can me modified to suit your needs. Check the Micro [keybindings](https://github.com/zyedidia/micro/blob/master/runtime/help/keybindings.md) tab for further information.

## What's next?

- [ ] Add guidelines for windows
- [ ] Adapt makefile for windows
- [ ] Add new color schemes (at least up to ten)
- [ ] Expand and improve syntax file
