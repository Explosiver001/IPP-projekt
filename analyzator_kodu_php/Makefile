PHP = php81
SOURCE = parse.php


d:
	$(PHP) -f $(SOURCE) -- -d <test_inputs/ex1.ippcode >flush.log

run: 
	$(PHP) -d open_basedir="." -f $(SOURCE) -- -h <test_inputs/zadani.ippcode 
	