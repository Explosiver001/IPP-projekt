PY = python3.10
SCRIPT = interpret.py

run:
	$(PY) $(SCRIPT) --source=test_inputs/main4.xml --input=input

test:
	rm -f out.html
	php81 test.php --directory=ipp-2023-tests/both/ --parse-script=../analyzator_kodu_php/parse.php --recursive > out.html

test_int:
	rm -f out.html
	php81 test.php --int-only --recursive --directory=ipp-2023-tests/interpret-only/ > out.html