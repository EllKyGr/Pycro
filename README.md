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
For instance pyrcula expands/modifies the original color scheme from
darcula.micro to adjust for the new statements.
Add to `~/.config/micro/colorschemes/` the `color_scheme_file.micro` either from
here, the Micro [repo](https://github.com/zyedidia/micro/tree/master/runtime/colorschemes) or a custom one.

### Sample
Several simple lines of code which encompasses the most common highlighted
cases for fast checking or test.

## How to set
1. Installing Micro:
	Micro 2.0.XX => https://github.com/benweissmann/getmic.ro
2. Plugins `micro -plugin install <plugin>`:
	- `aspell`: spell checking. `addpersonal` adds word to personal dict when cursor is placed under said word.

	- `filemanager`: adds a tree to visualize, open, create files and directories:
	    - `ctrl + e` then "tree:" open the file tree
	    - `left key` or `right key`: closes or collapses the directory
	    - `rename`: new name for selected file inside tree
        - `rm`: deletes file inside tree
	    - `touch`: creates file in the current path
	    - `mkdir`: creates directory in current path

	- `lsp`: adds language server for better coding style and formatting
		- Run `pip install python-lsp-server` for the lsp plugin to work
		- `alt + d` with cursor under a function returns the documentation
		- `alt + k` with cursor under function, object, etc returns brief
		- `ctrl + _` comments out the line. Undo the action with the same
		- `ctrl + space` kind of auto complete but with issues, however all
			         possible keywords are listed

	- `autofmt`: formats file content at save based on language. Until the new
	   [autofmt](https://github.com/a11ce/micro-autofmt) repo is updated with a `-plugin` command do this instead:
		1. `git clone git@github.com:a11ce/micro-autofmt.git`
		2. `cd` to micro-autofmt/ then `make`
		3. Currently only C/C++/C#, Python, Racket, JavaScript, Rust and Go are supported.
			   Every language require its specific formatter
		4. For Python run: `pip install` git+https://github.com/google/yapf.git
			   either directly or within environment

	- `quoter`: wraps the lines with double or single quotes


3. Settings and key bindings:
	after installing plugins edit, or create, the `settings.json` at `~/.config/micro`
	with the following options:
    ```
	{
	    "aspell.check": "on",
	    "aspell.lang": "en",
	    "colorcolumn": 80,
	    "colorscheme": "pyrcula",
	    "fmt-onsave": true,
	    "hlsearch": true,
	    "hltrailingws": true,
	    "savecursor": true

	    # lsp plugin will update `bindings.json` with the following options

	    "lsp.ignoreMessages": "LS message1 to ignore|LS message 2 to ignore|...",
	    "lsp.ignoreTriggerCharacters": "completion,signature",
	    "lsp.server": "python=pylsp",

	}
	```

Check the Micro [options](https://github.com/zyedidia/micro/blob/master/runtime/help/options.md) tab for further information
