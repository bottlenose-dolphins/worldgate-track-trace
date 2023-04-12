#!/bin/bash
# aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 283879969377.dkr.ecr.ap-southeast-1.amazonaws.com

#with db uri 
# images=('user' 'export' 'import' 'export-cont' 'import-cont' 'export-shipment' 'import-shipment' 'complex-scraper' 'prefix' 'vendor-mast' 'view-all' 'subscription', 'unloading-status' 'load-bl-doc', 'scheduler')

# images=('load-bl-doc')

# for image in "${images[@]}"
# do
#   echo "Pushing $image"

#   docker build -t "tracktrace_repo:core_$image" --file "Dockerfile-$image-prod" --build-arg db=$DB_URI . 
#   docker tag "tracktrace_repo:core_$image" "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:core_$image"
#   docker push "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:core_$image"

# done

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
images3=('vessel-location')


for image in "${images3[@]}"
do
  echo "Pushing $image"
  docker build -t "tracktrace_repo:core_$image" --file "Dockerfile-$image-prod" --build-arg VESSEL_API_KEY="4OrWAN1RwF9yIkFRVK9tE4zjhfNOXiWv6F3629ee" --build-arg LOCATION_API_KEY="1098|NvO69RTGk5mqoTeM5MxboTfq6A2MbV9bUH6UTSHU" --build-arg GMAPS_API_KEY="AIzaSyC24I-F1Ud-LVm7vK89V3MbCu8Ed-NWJ9A" . 
  docker tag "tracktrace_repo:core_$image" "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:core_$image"
  docker push "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:core_$image"
done






