# aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 283879969377.dkr.ecr.ap-southeast-1.amazonaws.com


# images=('export-cont' , 'import-cont' , 'export-shipment' , 'import-shipment' , 'complex-scraper' , 'prefix' , 'vendor-mast' , 'view-all')
# docker build -t "tracktrace_repo:fe" --file "Dockerfile-prod" --no-cache . 
docker build  -t "tracktrace_repo:fe" --file "Dockerfile-prod" --build-arg REACT_APP_API_ENDPOINT=$INT_LB_ENDPOINT --build-arg REACT_APP_GMAPS_KEY=$REACT_APP_GMAPS_KEY --no-cache .
docker tag "tracktrace_repo:fe" "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:fe"
docker push "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:fe"

