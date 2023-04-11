# aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 283879969377.dkr.ecr.ap-southeast-1.amazonaws.com
# images=('Ymlu' 'Cosco' 'Kmtc' 'One' 'Good' 'Cord')

# images=('Ymlu' 'Cosco' 'Kmtc' 'One', 'Maer', 'Sino')

images=('Maer')

for image in "${images[@]}"
do
  echo "Pushing $image"

  docker build -t "tracktrace_repo:scraper_$image" --file "Dockerfile-$image-prod" . 
  docker tag "tracktrace_repo:scraper_$image" "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:scraper_$image"
  docker push "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:scraper_$image"
  
done

# docker build -t "tracktrace_repo:scraper_Good" --file "Dockerfile-Good-prod" --build-arg GOOD_PW=$GOOD_PW --build-arg GOOD_UN=$GOOD_UN . 
# docker tag "tracktrace_repo:scraper_Good" "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:scraper_Good"
# docker push "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:scraper_Good"

# docker build -t "tracktrace_repo:scraper_Cord" --file "Dockerfile-Cord-prod" --build-arg CORD_UN=$CORD_UN --build-arg CORD_PW=$CORD_PW . 
# docker tag "tracktrace_repo:scraper_Cord" "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:scraper_Cord"
# docker push "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:scraper_Cord"