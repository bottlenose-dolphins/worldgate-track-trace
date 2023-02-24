# aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 283879969377.dkr.ecr.ap-southeast-1.amazonaws.com


images=('export-cont' , 'import-cont' , 'export-shipment' , 'import-shipment' , 'complex-scraper' , 'prefix' , 'vendor-mast' , 'view-all')
docker build -t "tracktrace_repo:fe4" --file "Dockerfile-prod" --no-cache . 
docker tag "tracktrace_repo:fe4" "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:fe4"
docker push "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:fe4"

