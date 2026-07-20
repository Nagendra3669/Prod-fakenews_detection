.PHONY: help install run-api run-frontend run-all

help:
	@echo "Available targets:"
	@echo "  make install         Install Python dependencies"
	@echo "  make run-api         Start the FastAPI backend"
	@echo "  make run-frontend    Start the frontend app"
	@echo "  make run-all         Show how to start both services"

install:
	python -m pip install -r app/requirements.txt

run-api:
	python main.py

run-frontend:
	python -m streamlit run frontend/app.py

run-all:
	@echo "Start the backend with: make run-api"
	@echo "Start the frontend with: make run-frontend"
