import argparse

from time import time

import numpy as np

from PIL import Image

from capture import PiCameraStream
from models import TensorFlowDetector


def main():

    stream = PiCameraStream()
    model = None
    if arg_options.detector:
        model = TensorFlowDetector(
            model=arg_options.detector,
            labels=arg_options.labels)

    try:
        stream.start()

        while not stream.stopped:
            if stream.frame is not None:
                image = stream.read()
                image = np.expand_dims(image, 0)
                if model is not None:
                    predictions = model.predict(image)
                    print("prediction", predictions)
                if arg_options.output:
                    Image.fromarray(image).save("{}/{}.jpg".format(arg_options.output, time()))

    except KeyboardInterrupt:
        stream.stop()


def get_parser():
    return argparse.ArgumentParser(
        description="Command line program to capture and process images from PiCamera")
    parser.add_argument(
        "-d", "--detector",
        help="Path to a frozen TensorFlow model in protobuf format (.pb)")
    parser.add_argument(
        "-l", "--labels",
        help="Path to a .txt file with one class name per line")
    parser.add_argument(
        "-o", "--output",
        help="Output path where captured images will be stored.")


if __name__ == "__main__":

    parser = get_parser()
    arg_options = parser.parse_args()

    main()
