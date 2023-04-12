env:
	python -m venv env
	
run:
	streamlit run .\DashBoard.py

install:
	pip install -r .\requirements.txt