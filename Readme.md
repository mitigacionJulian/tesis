# Requisitos minimos

* miktex  (https://miktex.org/download)
* python (https://www.python.org/downloads/)
* piments (pip install Pygments)

# Requisitos opcionales

* texstudio (windows)

# Compilacion con latexmk

Para utilizar latexmk debe instalar Perl (https://www.perl.org/get.html)

compilar

    latexmk -xelatex -shell-escape -silent -synctex=1 .\main.tex

limpiar

    latexmk -C

# Compilación con make

Debe instalar make

compilar

    make 

limpiar 

    make clean

# Compilación con xelatex

compilación

    xelatex   -shell-escape   main.tex
    biber main
    xelatex   -shell-escape   main.tex
    xelatex   -shell-escape   main.tex

# Texstudio

opciones > configurar TexStudio... > compilar 

    compilador por defecto: Latexmk
    Herramienta bibliografica por defecto: Biber

opciones > configurar TexStudio... > órdenes    

    Latexmk: latexmk.exe -xelatex -silent -shell-escape -synctex=1 %

# Compilación online

* overleaf.com

# errrores de compilación

En main.text cambie `\usepackage[no-math]{fontspec}` por `\usepackage{fontspec}`
