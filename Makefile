config:
	@cp .env.example .env

build:
	@sudo docker compose up --build

start:
	@sudo docker compose up

stop:
	@sudo docker compose down 

rmv: 
	@sudo docker compose down -v
