# GCP Redis
PROJECT_ID=docai-warehouse-demo
REGION=us-central1
# gcloud services enable --project=$PROJECT_ID networkconnectivity.googleapis.com
# gcloud services enable --project=$PROJECT_ID compute.googleapis.com
# gcloud services enable --project=$PROJECT_ID serviceconsumermanagement.googleapis.com
# gcloud services enable --project=$PROJECT_ID redis.googleapis.com

# gcloud network-connectivity service-connection-policies create memorystore-connection-policy\
#     --network=default\
#     --project=$PROJECT_ID\
#     --region=$REGION\
#     --service-class=gcp-memorystore-redis\
#     --subnets=https://www.googleapis.com/compute/v1/projects/$PROJECT_ID/regions/$REGION/subnetworks/default

# gcloud network-connectivity service-connection-policies list --region=$REGION --project=$PROJECT_ID

# gcloud redis instance create aidf-cache \
#     --project=$PROJECT_ID \
#     --region=$REGION \
#     --size=5 \
#     --network=projects/$PROJECT_ID/global/networks/default
