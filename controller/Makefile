.DEFAULT_GOAL := copy

.user    := pi
.machine := pi3.local
.env     := /home/pi/.virtualenvs/cv/bin/activate
.dir     := buddha

help:
	@echo ""
	@echo "Available commands :"
	@echo ""
	@echo "  make \t\t\t\tcopies current directory"
	@echo "  make copy\t\t\tcopies current directory"
	@echo "  make install\t\t\tinstalls Python dependencies"
	@echo ""

copy:
	rsync -r ./* $(.user)@$(.machine):~/$(.dir)

install: copy
	ssh $(.user)@$(.machine) " \
	source $(.env); \
	pip install -r $(.dir)/requirements.txt"

.PHONY: copy install
