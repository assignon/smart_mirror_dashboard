import time
import sqlalchemy as sa
import pickle
import numpy as np
import redis
import os
from dotenv import load_dotenv

load_dotenv('.env')


def daily_delete(db, redis_db):
    aws_success = False
    redis_success = False

    for _ in range(10):

        # Delete expired guests from AWS
        if aws_success is False:
            try:
                db.session.execute(f"""DELETE FROM Guest WHERE consent_expire_date < {int(time.time())} ;""")
                db.session.commit()
                aws_success = True
            except Exception:
                print("failed to delete from AWS")

        # Delete guest from Redis
        if redis_success is False:
            try:
                redis_db.delete_expired()
                redis_success = True
            except Exception:
                print("Failed to delete from Redis")

        if aws_success is True and redis_success is True:
            print("guests deleted")
            return

    print("Failed to delete guests")






# # Update the face recognitiopn model
# recognizer = pickle.loads(open('../face_recognition/models/face_recognizer.p', "rb").read())
#
# # get embeddings and labels from redis
# face_embeddings, face_ids = redis_db.get_vectors()
#
# # Train model
# recognizer.fit(np.array(face_embeddings), np.array(face_ids))
#
# # dump new model in pickle
# pickle.dump(recognizer, open('../face_recognition/models/face_recognizer.p', "wb"))
