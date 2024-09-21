start:
	echo "Starting..."
	docker compose up -d
	# Define a trap to stop the Docker container on script exit
	echo "Waiting 10 Seconds for the container to start..."
	sleep 10
	trap 'echo "Stopping..."; docker compose down' EXIT
	API_ENV=development PYTHONPATH=./src uvicorn src.main:app --reload --host 0.0.0.0 --port 8888

prod:
	API_ENV=production PYTHONPATH=./src uvicorn src.main:app --host 0.0.0.0 --port 8888

db:
	docker compose up

dev:
	API_ENV=development PYTHONPATH=./src uvicorn src.main:app --reload --host 0.0.0.0 --port 8888