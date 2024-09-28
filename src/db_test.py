import psycopg
import time

start_time = time.time()

print(f'started at {time.time()}')

conn = psycopg.connect("postgresql://saas_owner:fL5u2vhpXEZi@ep-white-lake-a77iql3q.ap-southeast-2.aws.neon.tech/saas?sslmode=require")

print(f'connection es {time.time() - start_time} seconds')

conn.close()