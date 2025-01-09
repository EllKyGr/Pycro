micro_dir := ~/.config/micro

.SILENT: install uninstall add clean
# print:
# 	ls $(micro_dir)
# 	(cd ~/.config/micro; echo "working directory: $$PWD"); \
# 	echo "makefile path directory: $$PWD"
install: add
	cp $$PWD/*.json $(micro_dir); cp colorschemes/*.micro $(micro_dir)/test_colorschemes; cp syntax/*.yaml $(micro_dir)/test_syntax
add:
	echo "Adding Pycro files at $(micro_dir)\nBindings and settings:"; ls $$PWD/*.json | cut -d'/' -f 7;
	echo "Colorscheme(s) at: $(micro_dir)/test_colorschemes"; mkdir -p $(micro_dir)/test_colorschemes; ls $$PWD/colorschemes | cut -d'.' -f 1;
	echo "Syntax file(s) at: $(micro_dir)/test_syntax"; mkdir -p $(micro_dir)/test_syntax; ls $$PWD/syntax/ | cut -d'.' -f 1;
uninstall:
	echo "Removing Pycro files"
	rm -fr ~/.config/micro/test_colorschemes
	rm -fr ~/.config/micro/test_syntax
	rm -f ~/.config/micro/first.json ~/.config/micro/second.json
	# rm -f ~/.config/micro/*.json
clean:
	rm -rf pycro/
