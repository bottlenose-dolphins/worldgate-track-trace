# aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 283879969377.dkr.ecr.ap-southeast-1.amazonaws.com


# images=('export-cont' , 'import-cont' , 'export-shipment' , 'import-shipment' , 'complex-scraper' , 'prefix' , 'vendor-mast' , 'view-all')

images=('export')

for image in "${images[@]}"
do
  echo "Pushing $image"

  docker build -t "tracktrace_repo:core_$image" --file "Dockerfile-$image-prod" . 
  docker tag "tracktrace_repo:core_$image" "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:core_$image"
  docker push "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:core_$image"
done
