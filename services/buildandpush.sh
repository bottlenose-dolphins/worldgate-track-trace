aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 283879969377.dkr.ecr.ap-southeast-1.amazonaws.com

docker buildx build -t "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:_core_complex_scraperv1.0_ARM" --file services/backend/core/Dockerfile-complex-scraper-prod --platform linux/arm64 --push .
