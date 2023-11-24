DOCKER_IMAGE=temp427/checkpoint-placer:0.1

lint:
	black src/ tests/
	isort src/ tests/
	flake8 src/ tests/
	mypy src/ tests/

test:
	export PYTHONPATH=./src; pytest --cov=src --cov-report=term-missing tests/

build-docker:
	docker build -t $(DOCKER_IMAGE) .

run-docker:
	docker run -p 10000:10000 $(DOCKER_IMAGE)

sanity-test-server:
	curl -X POST http://localhost:10000/server -H "content-type:application/json" -d '{"e1": "1","h": "5","graph": " digraph graphname{\n1->2\n2->3\n2->5\n5->2\n3->5}"}'
