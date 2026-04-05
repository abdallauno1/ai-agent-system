.PHONY: install run test lint docker-build

install:
	python -m pip install --upgrade pip && pip install -r requirements.txt

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest -q

docker-build:
	docker build -t ai-agent-system:latest .
