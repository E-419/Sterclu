import os, sys, pathlib
# This import sequence requires the other modules to be in the same /src directory
if __name__ == '__main__':
	from SearchBar import SearchBar
	from SearchView import SearchView
	from ScrollView import ScrollView
	from Icon import Icon
	
else:
	if 'src' in os.getcwd():
		from SearchBar import SearchBar
		from SearchView import SearchView
		from ScrollView import ScrollView
		from Icon import _Icon as Icon
		
	else:
		from src.SearchBar import SearchBar
		from src.SearchView import SearchView
		from src.ScrollView import ScrollView
		from src.Icon import _Icon as Icon