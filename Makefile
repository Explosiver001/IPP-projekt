pack:
	cd analyzator_kodu_php && zip xnovak3g.zip parse.php readme1.md parse_libs/*
	mv analyzator_kodu_php/xnovak3g.zip ./interpret_python/
	cd interpret_python && zip xnovak3g.zip interpret.py readme2.md int_libs/
	mv interpret_python/xnovak3g.zip ./