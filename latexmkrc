# latexmkrc — latexmk avec LuaLaTeX et Biber (tout est automatique).
#
#   latexmk main.tex          compile (relance seul LuaLaTeX / Biber si besoin)
#   latexmk -c                supprime les fichiers auxiliaires
#   latexmk -C                supprime aussi les PDF
#
# Quelle que soit l'option reçue (-pdf de TeXstudio, -lualatex, rien),
# c'est toujours LuaLaTeX qui compile.

$pdf_mode   = 4;
$lualatex   = 'lualatex -interaction=nonstopmode -synctex=1 -file-line-error %O %S';
$pdflatex   = $lualatex;
$bibtex_use = 2;
$clean_ext  = 'bbl run.xml synctex.gz';
