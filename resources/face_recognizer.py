"""
This module contains the recognition module and related functions.
"""
import os
from statistics import mode
import numpy as np
from tensorflow.keras.models import load_model
from numpy import expand_dims
from sklearn.preprocessing import Normalizer
from sklearn.neighbors import BallTree
from settings import redis_db


base_path = os.path.dirname(__file__)


class FaceRecognizer:
    """
    Class containing all fuctions related to recognizing faces.
    """
    def __init__(self):
        # get embeddings and labels from redis
        self.face_embeddings, self.face_ids = redis_db.get_vectors()
        print(set(self.face_ids))

        # 128-D vector (face data) setup
        self.embedder = load_model(os.path.join(base_path,
                                                "models/facenet_keras.h5"))

        if len(set(self.face_ids)) > 0:
            self.recognizer = BallTree(self.face_embeddings, leaf_size=10)

        # Settings
        self.treshold_osnn = .84
        self.radius = .82
        self.n_neighbors = 5

    def facenet(self, input_img):
        """Takes a face detection result and distils a
        128D vector set in euclidean space.

        Parameters:
        input_img (np.array): An image in the form of a numpy array

        Returns:
        np.array: A 128D array with data representing a face.
        float: the runtime of the function in seconds
        """
        # scale pixel values
        face_pixels = input_img.astype('float32')
        # standardize pixel values across channels (global)
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std

        # transform face into one sample
        samples = expand_dims(face_pixels, axis=0)
        # make prediction to get embedding
        yhat = self.embedder.predict(samples)
        normal_encoder = Normalizer(norm='l2')
        embedding = normal_encoder.transform(yhat)

        return embedding[0]

    def recognize_face(self, input_image):
        """
        This function expects a face embedding as input and runs it through an
        SVM trained on the known faces.
        If it matches to any of the known faces it returns the ID,
        otherwise it returns False.
        inputs:
        face_embedding, a numpy array with 128-D vactor in it.
        """
        # Check input format
        if not isinstance(input_image, (np.ndarray, np.generic)):
            return "Invalid input format"

        face_embedding = self.facenet(input_image)

        # if no faces in database return unknown
        if len(set(self.face_ids)) == 0:
            pred = 0
            return pred
        # Run Recognizer
        # get nearest neighbors to prediction point
        elif len(set(self.face_ids)) == 1:
            dist, ind = self.recognizer.query([face_embedding], k=20)
        else:
            dist, ind = self.recognizer.query([face_embedding], k=25)

        d_ratio = 1

        min_dist = np.min(dist[0])

        # check for the closest point with a different label
        # than the closest point
        for i, point in enumerate(ind[0]):
            if self.face_ids[ind[0][0]] != self.face_ids[point]:
                # Distance ratio is closest point divided by further point
                d_ratio = dist[0][0] / dist[0][i]
                break
        # Prediction threchold
        if d_ratio <= self.treshold_osnn or min_dist < self.radius:
            labels = []
            # Find N Nearest Neighbors
            for index in ind[0][:self.n_neighbors]:
                labels.append(self.face_ids[index])
            pred = mode(labels)
        else:
            pred = 0

        return pred


    def update_recognizer(self, new_embeddings, new_id, expire_date):
        """
        This function takes an array with face data and an id,
        and retrains the model.
        inputs:
        face_array, an array with face data in there in
        the form of numpy arrays.
        face_id, an int to be used for the face_array.
        """

        self.face_embeddings += new_embeddings
        self.face_ids += len(new_embeddings) * [new_id]
        redis_db.add_vectors(new_id, expire_date, new_embeddings)

        # Rebuild tree
        self.recognizer = BallTree(self.face_embeddings, leaf_size=10)

        return "Succes"


    def delete_id(self, input_id):
        """
        This function removes the embeddings for a certain face_id.
        input_id, an int representing a face id to be deleted.
        """

        for index, id_value in reversed(list(enumerate(self.face_ids))):
            # print(id_value)
            if int(id_value) == int(input_id):
                del self.face_embeddings[index]
                del self.face_ids[index]

        # delete data in redis
        redis_db.del_guest(input_id)

        # Rebuild tree
        self.recognizer = BallTree(self.face_embeddings, leaf_size=10)

    def get_trained_ids(self):
        """
        This function returns an array of the face id's
        currently in the dataset.
        """
        return set(self.face_ids)


