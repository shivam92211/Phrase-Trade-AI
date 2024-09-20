run:
	echo "Starting..."
	docker compose up -d
	# Define a trap to stop the Docker container on script exit
	trap 'echo "Stopping..."; docker compose down' EXIT
	uvicorn main:app --reload 


