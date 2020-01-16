# S3 GC
[![Docker Repository on Quay](https://quay.io/repository/verygoodsecurity/s3gc/status "Docker Repository on Quay")](https://quay.io/repository/verygoodsecurity/s3gc)

S3 cleaner for those who need more features than AWS Lifecycle provides
- 1 minute precision
- wildcards support

## Docker
```bash
docker run -i \
  -e AWS_ACCESS_KEY_ID="XXX"
  -e AWS_SECRET_ACCESS_KEY="XXX"
  -e BUCKET='my-bucket' \
  -e WILDCARD='logs/debug/app/' \
  -e HOURS=3 \
  quay.io/verygoodsecurity/s3gc:release-0.2.0 
```

## Kubernetes CronJob
```
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: s3gc
  namespace: s3gc
spec:
  schedule: 0 * * * *
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: Never
          containers:
          - image: quay.io/verygoodsecurity/s3gc:release-0.2.0
            name: s3gc
```

## Security
It is highly recommended to run this under a strict IAM role which has access 
only to certain operations in a single bucket. 

IAM Policy example TODO

- Locally, [aws-profile](https://github.com/jrstarke/aws-profile) can be used to 
generate temp credentials based on a role.
- In Kubernetes, use [EKS pod roles](https://aws.amazon.com/blogs/opensource/introducing-fine-grained-iam-roles-service-accounts/) 
or projects like [kiam](https://github.com/uswitch/kiam/) to delegate IAM role to a pod.