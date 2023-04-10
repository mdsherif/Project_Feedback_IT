env:
	python -m venv env
	
run:
	streamlit run .\app.py

install:
	pip install -r .\requirements.txt