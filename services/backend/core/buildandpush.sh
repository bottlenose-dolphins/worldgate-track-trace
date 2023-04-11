#!/bin/bash
# aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 283879969377.dkr.ecr.ap-southeast-1.amazonaws.com

#with db uri 
# images=('user' 'export' 'import' 'export-cont' 'import-cont' 'export-shipment' 'import-shipment' 'complex-scraper' 'prefix' 'vendor-mast' 'view-all' 'subscription', 'unloading-status' 'load-bl-doc', 'scheduler')

images=('subscription')

for image in "${images[@]}"
do
  echo "Pushing $image"

  docker build -t "tracktrace_repo:core_$image" --file "Dockerfile-$image-prod" --build-arg db=$DB_URI . 
  docker tag "tracktrace_repo:core_$image" "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:core_$image"
  docker push "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:core_$image"

done

# noti complex
#twilio sid, client
# images2=('notification-complex')

# # images=('user')

# for image in "${images2[@]}"
# do
#   echo "Pushing $image"
#   docker build -t "tracktrace_repo:core_$image" --file "Dockerfile-$image-prod" --build-arg twilio_sid=$twilio_sid --build-arg twilio_token=$twilio_token .
#   docker tag "tracktrace_repo:core_$image" "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:core_$image"
#   docker push "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:core_$image"
# done


# # //vessel location
# #gmap, vessel, location
# images3=('vessel-location')

# # images=('user')

# for image in "${images3[@]}"
# do
#   echo "Pushing $image"
#   docker build -t "tracktrace_repo:core_$image" --file "Dockerfile-$image-prod" --build-arg VESSEL_API_KEY=$VESSEL_API_KEY --build-arg LOCATION_API_KEY=$LOCATION_API_KEY --build-arg GMAPS_API_KEY=$REACT_APP_GMAPS_KEY . 
#   docker tag "tracktrace_repo:core_$image" "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:core_$image"
#   docker push "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:core_$image"
# done






