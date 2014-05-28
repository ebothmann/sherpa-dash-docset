default:
	@echo Valid build targets:
	@echo "  * fetch"
	@echo "  * build"
	@echo "  * install"

fetch:
	wget -r --no-parent -P sherpa.docset/Contents/Resources/Documents -p -- https://sherpa.hepforge.org/doc/SHERPA-MC-2.1.0.html

build:
	./sherpadoc2set.py

install:
	open -aDash sherpa.docset