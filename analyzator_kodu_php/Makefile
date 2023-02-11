PHP = php81
SOURCE = parse.php

r:
	@$(PHP) -f $(SOURCE) ##<test_inputs/zadani.ippcode

d:
	@$(PHP) -f $(SOURCE) -- -d <test_inputs/zadani.ippcode >flush.log

run: 
	$(PHP) -d open_basedir="." -f $(SOURCE) -- -h <test_inputs/zadani.ippcode 
	