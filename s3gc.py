import datetime
import boto3
import pytz
import os
import fnmatch

s3 = boto3.client('s3')
S3_BATCH = 1000

BUCKET = os.environ['BUCKET']
WILDCARD = os.environ.get('WILDCARD', '')
PREFIX = os.path.dirname(WILDCARD.split("*")[0].split('?')[0].split('[')[0])
DRY_RUN = os.environ.get('DRY_RUN', 'true').lower() in ('true', '1')

NOW = datetime.datetime.now(tz=pytz.UTC)
DAYS = int(os.environ.get('DAYS', 0))
HOURS = int(os.environ.get('HOURS', 0))
MINUTES = int(os.environ.get('MINUTES', 0))
PAST = NOW - datetime.timedelta(days=DAYS, hours=HOURS, minutes=MINUTES)


def main():
    do_gc(BUCKET, PREFIX, WILDCARD, DRY_RUN)


def do_gc(bucket, prefix, wildcard, dry_run):
    to_delete = []
    for obj in get_objects_to_delete(bucket, prefix, wildcard):
        to_delete.append({'Key': obj['Key']})

        if len(to_delete) == S3_BATCH:
            delete_objects(bucket, to_delete, dry_run)
            to_delete.clear()

    delete_objects(bucket, to_delete, dry_run)
    print('Done.')


def get_objects_to_delete(bucket, prefix, wildcard):
    kwargs = dict(Bucket=bucket, Prefix=prefix)
    while True:
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            if fnmatch.fnmatch(obj['Key'], wildcard) and (obj['LastModified'] < PAST):
                yield obj

        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break


def delete_objects(bucket, objects, dry_run=True):
    if not objects:
        print(f"Nothing to delete")
        return
    if dry_run:
        print(f"Dry-run deleting {objects}")
    else:
        print(f"Deleting {objects}")
        s3.delete_objects(Bucket=bucket, Delete={'Objects': objects})


if __name__ == "__main__":
    main()