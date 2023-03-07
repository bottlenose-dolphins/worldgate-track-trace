# aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 283879969377.dkr.ecr.ap-southeast-1.amazonaws.com

# images=('Ymlu' , 'Cosco' , 'Kmtc' , 'One' , 'Good' , 'Cord')

images=('Ymlu' , 'Cosco' , 'Kmtc' , 'One')

for image in "${images[@]}"
do
  echo "Pushing $image"

  docker build -t "tracktrace_repo:scraper_$image" --file "Dockerfile-$image-prod" . 
  docker tag "tracktrace_repo:scraper_$image" "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:scraper_$image"
  docker push "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:scraper_$image"
  
done