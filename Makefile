# Default platform for Mac M2 Silicon
DEFAULT_PLATFORM=linux/arm64
PLATFORM?=$(DEFAULT_PLATFORM)
PLATFORMS=linux/amd64,linux/arm64

# Image name for local testing
IMAGE_NAME=epub_to_audio_localtts
TAG=latest

# Target for building the image locally for a single platform
build-local:
	docker buildx build --platform $(PLATFORM) -t $(IMAGE_NAME):$(TAG) --load .

# Target for testing the local build
test-local:
	docker run --rm -v $(PWD)/input:/app/input -v $(PWD)/output:/app/output $(IMAGE_NAME):$(TAG) /bin/bash -c "python3 /app_src/main.py /app/output /app/input"

# Target for building and pushing the image to the repository for multiple platforms
build-and-push:
	docker buildx build --platform $(PLATFORMS) -t ghcr.io/the-digital-dev/epub_to_audio_localtts:$(TAG) --push .

# Target for building and pushing the image specifically for the production server (linux/amd64)
build-prod:
	docker buildx build --platform linux/amd64 -t ghcr.io/the-digital-dev/epub_to_audio_localtts:$(TAG) --push .

# Target for deploying the application with Docker Compose
deploy:
	docker-compose up -d

# Master target to run all steps in order
all: build-local test-local build-and-push

.PHONY: build-local test-local build-and-push build-prod deploy all
