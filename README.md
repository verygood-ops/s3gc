# S3 GC
[![Docker Repository on Quay](https://quay.io/repository/verygoodsecurity/s3gc/status "Docker Repository on Quay")](https://quay.io/repository/verygoodsecurity/s3gc)

S3 cleaner for those who need a schedule more precise than AWS Lifecycle.

## Usage
```bash
docker run -i \
  -e AWS_ACCESS_KEY_ID="XXX"
  -e AWS_SECRET_ACCESS_KEY="XXX"
  -e BUCKET='my-bucket' \
  -e WILDCARD='logs/debug/app/' \
  -e HOURS=3 \
  quay.io/verygoodsecurity/s3gc:release-X.X.X 
```

## Kubernetes CronJob
TODO

## Security
It is highly recommended to run this under a strict role which has only access 
to delete operation in a single bucket. 

Policy example TODO

 - Locally, [aws-profile](https://github.com/jrstarke/aws-profile) can be used to 
generate temp credentials based on a role.
- In Kubernetes, use projects like [kiam](https://github.com/uswitch/kiam/) or 
[EKS pod roles](https://aws.amazon.com/blogs/opensource/introducing-fine-grained-iam-roles-service-accounts/)
to delegate role to a pod.