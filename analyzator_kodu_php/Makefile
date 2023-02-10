PHP = php81
SOURCE = parse.php


d:
	$(PHP) -f $(SOURCE) -- -d <test_inputs/example_demo.ifjcode >flush.log

run: 
	$(PHP) -d open_basedir="." -f $(SOURCE) -- -h <test_inputs/example_demo.ifjcode 
	