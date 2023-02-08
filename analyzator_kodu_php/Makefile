PHP = php81
SOURCE = parse.php


run1:
	$(PHP) $(SOURCE) <test_inputs/example_demo.ifjcode 

run: 
	$(PHP) -d open_basedir="." -f $(SOURCE) -- -h <test_inputs/example_demo.ifjcode 
	