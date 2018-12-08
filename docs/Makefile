src = $(wildcard *.md)
htmls = $(src:.md=.html)
pdfs = $(src:.md=.pdf)

pdf: $(pdfs)
all: html pdf
html: $(htmls)

%.pdf: %.md
	pandoc \
		-t beamer \
		-V theme=Warsaw \
		--toc \
		-s \
		$< \
		-o $@

%.html: %.md
	pandoc \
		-t revealjs \
		-V revealjs-url="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.7.0" \
		-V theme=sky \
		-s \
		$< \
		-o $@


.PHONY: clean

clean:
	rm -f $(pdfs) $(htmls)
