import redis
from timeit import default_timer as timer
import numpy as np
import time
import pickle


class RedisDatabase:

    def __init__(self, host, port, password):
        self.session = redis.StrictRedis(host=host, port=port, password=password)

    def del_guest(self, guest_id):
        self.session.delete("guest:" + str(guest_id))
        self.session.zrem("guest_ids", guest_id)

    def add_vector(self, guest_id, expire_time, vector):
        """ 1 vector toevoegen"""
        encoded = vector.tobytes()
        self.session.rpush("guest:" + str(guest_id), encoded)
        self.session.expireat("guest:" + str(guest_id), expire_time)
        self.session.zadd("guest_ids", {guest_id: expire_time})

    def add_vectors(self, guest_id, expire_time, embeddings):
        """lijst van vectors toevoegen"""
        encoded_embeddings = [embedding.tobytes() for embedding in embeddings]
        self.session.rpush("guest:" + str(guest_id), *encoded_embeddings)
        self.session.expireat("guest:" + str(guest_id), expire_time)
        self.session.zadd("guest_ids", {guest_id: expire_time})

    def create_dataset(self, m):
        self.session.flushall()
        for i in range(1, m + 1):
            for _ in range(1000):
                self.add_vector(i, int(time.time() + 36000), np.random.rand(128).astype(np.float32))

    def get_vectors(self):
        """
        Get a tuple first item is list of numpy arrays, second item is a list with corresponding guest_id
        """
        pipe = self.session.pipeline()
        start = timer()
        vectors = []
        labels = []
        guest_ids = self.session.zrange("guest_ids", 0, -1)
        guest_ids = [int(guest_id.decode("utf-8")) for guest_id in guest_ids]

        for guest_id in guest_ids:
            pipe.lrange("guest:" + str(guest_id), 0, -1)

        results = pipe.execute()
        for idx, guest_id in enumerate(guest_ids):
            for encoded_vector in results[idx]:
                vector = np.frombuffer(encoded_vector, dtype=np.float32)
                vectors.append(vector)
                labels.append(guest_id)

        end = timer()

        print("total time getting vectors is " + str(end - start) + "\n")
        return vectors, labels

    def reset(self):
        self.session.flushall()

    def delete_expired(self):
        self.session.zremrangebyscore("guest_ids", min=0, max=int(time.time()))

    def data_transfer(self):
        """Transfer current dataset to redis"""

        self.session.flushall()

        labels = pickle.load(open("face_recognition/pickles/face_ids.p",  'rb'))
        embeddings = pickle.load(open("face_recognition/pickles/face_embeddings.p", 'rb'))

        for i in range(len(embeddings)):
            self.add_vector(labels[i], int(time.time()) + 60*60*24*365, embeddings[i])

    def get_guests(self):
        bytes_ids = self.session.zrange("guest_ids", 0, -1)
        guest_ids = [byte_id.decode('utf-8') for byte_id in bytes_ids]
        return guest_ids

    def get_cache_ids(self):
        bytes_ids = self.session.zrange("cache_ids", 0, -1)
        cache_ids = [int(byte_id) for byte_id in bytes_ids]
        return cache_ids

    def add_unknown_embeddings(self, embeddings):
        cache_id = str(self.session.incr('cache_id'))
        key = "unknown_embeddings:" + cache_id
        embeddings = [embedding.tobytes() for embedding in embeddings]
        expire_time = int(time.time()) + 60*60*24
        self.session.rpush(key, *embeddings)
        self.session.expireat(key, expire_time)
        self.session.zadd("cache_ids", {cache_id: expire_time})

    def get_cache_ids_with_unixtime(self):
        """" voor webapplicatie die de onbekende embeddings ophaalt eigenlijk niet de embeddings zelf maar de ids +
        tijden van de cache waarin de embeddings opgeslagen zijn als er niks is komt hier een lege lijst uit"""
        cache_id_in_bytes_with_unixtime = self.session.zrange('cache_ids', 0, -1, withscores=True)
        cache_id_with_unixtime = [(pair[0].decode('utf-8'), pair[1]) for pair in cache_id_in_bytes_with_unixtime]
        return cache_id_with_unixtime

    def label_unknown_embeddings(self, cache_id, guest_id):
        """Voegt de unknown embeddings toe aan de aangewezen gast en verwijdert de key waarin de unkown embeddings
        stonden"""
        embeddings = self.session.lrange('unknown_embeddings:' + str(cache_id), 0, -1)
        self.session.rpush('guest:' + str(guest_id), *embeddings)
        self.session.zrem('cache_ids', cache_id)
        self.session.delete('unknown_embeddings' + str(cache_id))

    def delete_all_unknowns(self):
        highest_id = int(self.session.get('cache_id'))
        ids = ["unknown_embeddings:" + str(i) for i in range(1, highest_id + 1)]
        self.session.delete('cache_ids', *ids)
        self.session.set('cache_id', 0)

    def delete_unknown_cache(self, cache_id):
        self.session.delete("unknown_embeddings:" + str(cache_id))
        self.session.zrem('cache_ids', cache_id)



