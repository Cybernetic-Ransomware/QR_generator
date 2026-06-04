.PHONY: up down restart logs build

up:
	docker compose -f docker-compose-traefik.yml up -d --build

down:
	docker compose -f docker-compose-traefik.yml down

restart: down up

logs:
	docker logs -f qr_web

build:
	docker compose -f docker-compose-traefik.yml build
