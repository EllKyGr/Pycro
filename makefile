.SILENT: all micro checksum pycro u-pycro u-micro add clean plugins auto-fmt python lsp yapf plug-fix darcula monokai catpuccin-mocha
.PHONY: all micro checksum pycro u-pycro u-micro add clean plugins auto-fmt python lsp yapf plug-fix darcula monokai catpuccin-mocha

micro_dir := ~/.config/micro
SHA := $(shell curl -s https://getmic.ro | shasum -a 256 | cut -d' ' -f 1)
plugins := aspell filemanager lsp runit manipulator quoter cheat snippets
colorschemes := darcula monokai catpuccin-mocha

all: micro pycro python plugins plug-fix
	echo "\n===== All Pycro files installed! =====\n\n'make clean' => removes cloned repository and its contents\n\
	      \n'make u-pycro' => removes Pycro files.\
	      \n'make u-micro' => removes both Micro and Pycro from your system\n\
	      \nWARNING: 'make clean' will relocate makefile to parent directory,\
	      \ndeleting it will unable the use of former commands!"

micro: checksum
	cd /usr/bin; echo "\nInstalling Micro at => $$PWD\n"; \
	curl https://getmic.ro | sudo bash;

checksum:
ifeq ($(SHA), 45e188ef0d5300cb04dcdece3934fa92f47b7581125c615a8bfae33ac7667a16)
	echo "===== Micro quick script available =====";
else
	echo $(error ERROR: Unable to verify script rerun makefile later on);
endif

pycro: add
	cp 	micro-set_bind/*.json $(micro_dir); cp colorschemes/*.micro $(micro_dir)/colorschemes; cp syntax/*.yaml $(micro_dir)/syntax
add:
	echo "===== Adding Pycro files =====\nConfiguration files at: $(micro_dir)"; echo $$PWD/micro-set_bind/*.json | grep -o '[a-z]*\.json'
	echo "\nColorscheme(s) at: $(micro_dir)/colorschemes"; mkdir -p $(micro_dir)/colorschemes; echo $$PWD/colorschemes/*.micro | grep -o '[a-z-]*\.micro'; \
	echo "\nSyntax file(s) at: $(micro_dir)/syntax"; mkdir -p $(micro_dir)/syntax; echo $$PWD/syntax/*.yaml | grep -o '[a-z0-9]*\.yaml'

python: lsp yapf
	echo "\n===== $^ installed! ====="
lsp:
	echo "\n===== Installing $@ =====\n"; \
	pip install python-lsp-server;

yapf:
	echo "\n===== Installing $@ =====\n"; \
	pip install git+https://github.com/google/yapf.git;

plugins: auto-fmt
	micro -plugin install $(plugins);

auto-fmt:
	echo "\n===== Installing plugins ====="; mkdir auto-fmt; touch auto-fmt/makefile;
	echo "autofmt:\n\tgit clone --quiet git@github.com:a11ce/micro-autofmt.git" > auto-fmt/makefile; \
	# Clone autofmt repository;   copy its files to micro plug
	cd auto-fmt/; $(MAKE) -s autofmt; cd micro-autofmt/; $(MAKE) -s install
	# Remove cloned repository
	rm -rf auto-fmt;

plug-fix:
	curl -s https://raw.githubusercontent.com/NicolaiSoeborg/manipulator-plugin/refs/heads/master/manipulator.lua -o manipulator.lua; \
	mv manipulator.lua $(micro_dir)/plug/manipulator; \
	sed -i 's#/micro-cheat/#/cheat/#g' $(micro_dir)/plug/cheat/main.lua;

u-pycro: json $(colorschemes)
	echo "===== Removing Pycro files ====="; \
	echo "Color schemes removed: $(colorschemes)"; \
	rm -f $(micro_dir)/syntax/python3.yaml;

$(colorschemes):
	rm -f $(micro_dir)/colorschemes/$@

json:
	echo "===== JSON files may contain additional user preferences ====="; \
	rm -i $(micro_dir)/*.json;

u-micro:
	cd /usr/bin; echo "Attempting to remove Micro from $$PWD"; sudo rm -i micro; \
	cd ~/.config/; echo "Removing Micro config from $$PWD"; rm -rf micro/;

clean:
	rm -rf colorschemes/ syntax/ micro-set_bind README.md test_sample.py; \
	echo "'makefile' moved to parent directory"; cd ../; mv Pycro/makefile ./; rm -rf Pycro/;
