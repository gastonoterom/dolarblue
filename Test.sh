# Run all tests & coverage
coverage run -m unittest discover -v -s Test -p "*_test.py"

# Turn coverage to html
coverage html