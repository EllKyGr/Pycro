.SILENT: pycro checksum install uninstall add clean
.PHONY: pycro checksum install uninstall add clean

micro_dir := ~/.config/micro
SHA := $(shell curl -s https://getmic.ro | shasum -a 256 | cut -d' ' -f 1)

all: pycro install
	echo "All Pycro files installed.\nRun 'make uninstall' to remove them including Micro.\
	      \nRun 'make clean' to remove the cloned repository and its contents"

pycro: checksum
	cd /usr/bin; echo "Installing Micro at $$PWD\n"; \
	curl https://getmic.ro | sudo bash;

checksum:
	ifeq ($(SHA), 45e188ef0d5300cb04dcdece3934fa92f47b7581125c615a8bfae33ac7667a16)
		echo "Requering Micro quick script..."; \
		echo "\nProceding with installation";
	else
		echo $(error ERROR: Unable to verify script rerun makefile later on);
	endif

install: add
	cp $$PWD/micro-set_bin/*.json $(micro_dir); cp colorschemes/*.micro $(micro_dir)/colorschemes; cp syntax/*.yaml $(micro_dir)/syntax
add:
	echo "Adding Pycro files at $(micro_dir)\nBindings and settings:"; ls $$PWD/micro-set_bin/*.json | cut -d'/' -f 7; \
	echo "Colorscheme(s) at: $(micro_dir)/test_colorschemes"; mkdir -p $(micro_dir)/colorschemes; ls $$PWD/colorschemes | cut -d'.' -f 1; \
	echo "Syntax file(s) at: $(micro_dir)/test_syntax"; mkdir -p $(micro_dir)/syntax; ls $$PWD/syntax/ | cut -d'.' -f 1; \

uninstall:
	echo "Removing Pycro files"; \
	rm -f ~/.config/micro/colorschemes/*_py.micro; \
	rm -f ~/.config/micro/syntax/python3.yaml; \
	rm -f ~/.config/micro/*.json; \
	cd /usr/bin; echo "Attempting to remove Micro from $$PWD"; rm -i micro;

clean:
	rm -rf colorschemes/ syntax/ micro-set_bin/ README.md test_sample.py makefile
