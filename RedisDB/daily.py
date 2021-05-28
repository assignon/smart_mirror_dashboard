import time
import sqlalchemy as sa
import pickle
import numpy as np
from settings import redis_db
import os
from dotenv import load_dotenv

load_dotenv('.env')

"""AWS CONNECTIE"""
username = os.getenv('AWS_USERNAME')
password = os.getenv('AWS_PASSWORD')
host = os.getenv('AWS_HOST')
db_name = os.getenv('AWS_DB_NAME')

connection_url = f'mysql+mysqldb://{username}:{password}@{host}/{db_name}'

engine = sa.create_engine(connection_url, echo=True)

# Delete guest from AWS
with engine.connect() as con:
    con.execute(f"""DELETE FROM Guest WHERE consent_expire_date < {int(time.time())} ;""")

# remove expired guests
redis_db.delete_expired()

# remove all unknown embeddings
redis_db.delete_all_unknowns()

# Update the face recognitiopn model
recognizer = pickle.loads(open('../face_recognition/models/face_recognizer.p', "rb").read())

# get embeddings and labels from redis
face_embeddings, face_ids = redis_db.get_vectors()

# Train model
recognizer.fit(np.array(face_embeddings), np.array(face_ids))

# dump new model in pickle
pickle.dump(recognizer, open('../face_recognition/models/face_recognizer.p', "wb"))
