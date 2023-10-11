pack:
	cd analyzator_kodu_php && zip xnovak3g.zip parse.php parse_libs/*.php
	mv analyzator_kodu_php/xnovak3g.zip ./interpret_python/
	cd interpret_python && zip xnovak3g.zip interpret.py readme2.pdf int_libs/*.py rozsireni
	mv interpret_python/xnovak3g.zip ./
