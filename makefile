.SILENT: all micro checksum pycro u-pycro u-micro add clean plugins auto-fmt python lsp yapf plug-fix
.PHONY: all micro checksum pycro u-pycro u-micro add clean plugins auto-fmt python lsp yapf plug-fix

micro_dir := ~/.config/micro
SHA := $(shell curl -s https://getmic.ro | shasum -a 256 | cut -d' ' -f 1)
plugins := aspell filemanager lsp runit manipulator quoter cheat snippets

all: micro pycro python plugins plug-fix
	echo "All Pycro files installed.\n'make clean' removes cloned repository and its contents\
	      \n'make u-pycro' removes Pycro files.\
	      \n'make u-micro' removes both Micro and Pycro from your system\
	      \nWARNING: 'make clean' may invalidate the removal of both Micro and Pycro\
	      \nthrough previously mentioned make commands if makefile is deleted!"

micro: checksum
	cd /usr/bin; echo "Installing Micro at $$PWD"; \
	curl https://getmic.ro | sudo bash;

checksum:
	ifeq ($(SHA), 45e188ef0d5300cb04dcdece3934fa92f47b7581125c615a8bfae33ac7667a16)
		echo "Micro quick script available"; \
	else
		echo $(error ERROR: Unable to verify script rerun makefile later on);
	endif

pycro: add
	cp 	micro-set_bin/*.json $(micro_dir); cp colorschemes/*.micro $(micro_dir)/colorschemes; cp syntax/*.yaml $(micro_dir)/syntax
add:
	echo "Adding Pycro files at $(micro_dir)\nBindings and settings:"; ls $$PWD/micro-set_bin/*.json | tail -2; \
	echo "Colorscheme(s) at: $(micro_dir)/colorschemes"; mkdir -p $(micro_dir)/colorschemes; ls $$PWD/colorschemes | tail; \
	echo "Syntax file(s) at: $(micro_dir)/syntax"; mkdir -p $(micro_dir)/syntax; ls $$PWD/syntax/ | tail;

python: lsp yapf
	echo "$^ installed"
lsp:
	echo "Installing $@"; \
	pip install python-lsp-server;

yapf:
	echo "Installing $@"; \
	pip install git+https://github.com/google/yapf.git;

plugins: auto-fmt
	micro -plugin install $(plugins);

auto-fmt:
	echo "Installing plugins"; mkdir auto-fmt; touch auto-fmt/makefile;
	echo "autofmt:\n\tgit clone git@github.com:a11ce/micro-autofmt.git\
	      \nclean:\n\tcd ../; rm -r auto-fmt" > auto-fmt/makefile; \
	# Clone autofmt repository;   copy its files to micro plug
	cd auto-fmt/; $(MAKE) -s autofmt; cd micro-autofmt/; $(MAKE) -s install; \
	# Remove cloned repository
	$(MAKE) -s clean;

plug-fix:
	curl -s https://raw.githubusercontent.com/NicolaiSoeborg/manipulator-plugin/refs/heads/master/manipulator.lua -o manipulator.lua; \
	mv manipulator.lua $(micro_dir)/plug/manipulator; \
	sed -i 's#/micro-cheat/#/cheat/#g' $(micro_dir)/plug/cheat/main.lua;

u-pycro: json
	echo "Removing Pycro files"; \
	rm -f $(micro_dir)/colorschemes/*_py.micro $(micro_dir)/syntax/python3.yaml;

json:
	echo "NOTE: JSON files may contain additional user preferences"; \
	rm -i $(micro_dir)/*.json;

u-micro:
	cd /usr/bin; echo "Attempting to remove Micro from $$PWD"; sudo rm -i micro; \
	cd ~/.config/; echo "Removing Micro config from $$PWD"; rm -rf micro/;

clean:
	rm -rf colorschemes/ syntax/ micro-set_bind README.md test_sample.py; \
	echo "Attempting to remove makefile... "; rm -i makefile;
