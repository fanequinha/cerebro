import abc

import numpy as np
import tensorflow as tf


class TensorFlowModel(abc.ABC):
    """
    Base class for all perception models.

    A TensorFlowModel takes care of:
        - Loading a TensorFlow graph from a trained model.
        - Setting up a TensorFlow session.
        - Extracting information from the graph.
        - Postprocessing the extracted information.
    """

    def __init__(self, model_path, labels, input_node="input", output_nodes=["output"]):
        """
        :param model_path:
        :param input_node:
        :param labels:
        :param output_node:
        """
        self.model_path = model_path
        self.labels = labels
        self.input_node = input_node
        self.output_nodes = output_nodes

    def load_graph(self):
        """ Loads and import a TensorFlow graph from a frozen model.
        :param model_path:
            Path to a frozen TensorFlow model in protobuf format (.pb).
        """
        self.graph = tf.Graph()

        graph_def = tf.GraphDef()

        with open(self.model_path, "rb") as f:
            graph_def.ParseFromString(f.read())

        with self.graph.as_default():
            # name="" is used to prevent TensorFlow's default prefix: "import/"
            tf.import_graph_def(graph_def, name='')

        self.input_tensor = self.graph.get_tensor_by_name("{}:0".format(self.input_node))
        self.output_tensors = [self.graph.get_tensor_by_name("{}:0".format(x)) for x in self.output_nodes]

    def setup_session(self, warm_start=True):
        """ Create and save a TensorFlow session with optional warm start.
        :param warm_start:
        :return:
        """
        self.session = tf.Session(graph=self.graph)

        if warm_start:
            self.session.run(
                self.output_tensors,
                {self.input_tensor: np.random.rand(128, 128, 3)})

    def get_predictions(self, image):
        """
        :param image:
        :return:
        """
        predictions = self.session.run(
            self.output_tensors,
            {self.input_tensor: image})

        return predictions

    @abc.abstractmethod
    def postprocess_predictions(self, predictions):
        pass
