.PHONY: all build deploy


all:
	make build
	make deploy


build:
	npm run build:prod


deploy:
	ssh -p 5522 root@yx.atomse.net 'mkdir -p /app/covid19/frontend'
	rsync -avP --delete -e 'ssh -p 5522' ./dist/ root@yx.atomse.net:/app/covid19/frontend
