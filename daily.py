import time
from dotenv import load_dotenv

load_dotenv('.env')


def daily_delete(db, redis_db):
    aws_success = False
    redis_success = False

    for _ in range(2):

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

        # aws promises a maximum of 22 minutes downtime per month, so on failure we wait 22 minutes and try to delete
        # the data agaain
        time.sleep(60*22)

    print("Failed to delete guests")
