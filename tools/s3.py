import boto
import boto.s3.connection
access_key = 'D73D59LO7N4D20DPMF99'
secret_key = 'WmnqcbDLzZCyqt8N0TuqNDKjqMEleYsCsuNDiST0'
bucket_name = 'geuvadis'
# gateway = '192.168.20.101'
gateway = 'griffin-objstore.opensciencedatacloud.org'

# create connection

conn = boto.connect_s3(
       aws_access_key_id = access_key,
       aws_secret_access_key = secret_key,
       port = 443,
       host = gateway,
       calling_format = boto.s3.connection.OrdinaryCallingFormat(),
       )

bucket = conn.get_bucket(bucket_name)

# for keys in bucket.list():
#     # print dir(keys)
#     print keys.name
#     # print keys.size
#     # print keys.get_path()
#     # print keys.metadata
#     # print keys.md5

prefix = "/asgc-geuvadis/"

key = bucket.get_key('geuvadis_public.test')
key.get_contents_to_filename('geuvadis_public.test')
print key
print "path="+prefix+key.name+" size="+str(key.size)+ " checksum="+key._get_md5()
