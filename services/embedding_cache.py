import os
import pickle


class EmbeddingCache:

    def save_metadata(self, path, data):

        os.makedirs(
            os.path.dirname(path),
            exist_ok=True
        )

        with open(path, "wb") as f:

            pickle.dump(data, f)

    def load_metadata(self, path):

        with open(path, "rb") as f:

            return pickle.load(f)