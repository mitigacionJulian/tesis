main:
        xelatex   -shell-escape   main.tex
        biber main
        xelatex   -shell-escape   main.tex
        xelatex   -shell-escape   main.tex
        make clean

.PHONY : clean

clean:
        latexmk -C