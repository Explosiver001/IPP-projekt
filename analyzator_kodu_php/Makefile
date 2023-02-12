PHP = php81
SOURCE = parse.php

basic:
	@$(PHP) -f $(SOURCE) 

d:
	@$(PHP) -f $(SOURCE) -- <test_inputs/zadani.ippcode

run: 
	$(PHP) -d open_basedir="." -f $(SOURCE) -- -h <test_inputs/zadani.ippcode 

pack:
	zip xnovak3g.zip parse.php parse_libs/*
