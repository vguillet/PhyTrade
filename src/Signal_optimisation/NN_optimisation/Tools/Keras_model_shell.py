
################################################################################################################
"""
Keras network model shell class built to experiment with various network structures and ease testing
"""

# Built-in/Generic Imports
import sys

# Libs
import matplotlib.pyplot as plt

# Own modules
from src.Tools.Colours_and_Fonts import cf

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

################################################################################################################


class Model_shell:
    def __init__(self,
                 model,
                 x_train, y_train,
                 x_test, y_test,
                 optimiser,
                 metrics,
                 train_test_split=0.1,
                 loss_function='categorical_crossentropy'):
        """
        Compile the model

        :param x_train: x training data
        :param y_train: y training data (target)

        :param x_test: x testing data
        :param y_test: y testing data (target)

        :param optimiser: Optimiser to be used
        :param train_test_split: Data split to be used for training and testing
        """
        # --> Initiate placeholder variables
        self.nb_epoch = None
        self.history = None
        self.score = None

        # --> Record self variables
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test

        self.train_test_split = train_test_split

        print("_______________________________________________")
        print("--> Data loaded in shell:")
        print(">", self.x_train.shape, "training samples x")
        print(">", self.y_train.shape, "training samples y\n")

        print(">", self.x_test.shape, "testing samples x")
        print(">", self.y_test.shape, "testing samples y")
        print("_______________________________________________\n")

        # --> LSTM network compilation
        self.model = model

        # --> Generate and output model summary
        self.model.summary()

        # --> Compile model
        self.model.compile(loss=loss_function, optimizer=optimiser, metrics=metrics)

        print("--> Compile Model: success")
        print("> Loss function:", loss_function)
        print("> Optimiser:", optimiser)
        print("> Metric:", metrics)

    def fit_model(self, nb_epoch, batch_size=None, validation_split=0.2, verbose=1):
        """
        Fit the model

        :param nb_epoch: Number of epoch
        :param batch_size: Number of samples, set automatically for lstm/rnn etc...
        :param verbose: Specifies verbosity mode(0 = silent, 1= progress bar, 2 = one line per epoch)
        :param validation_split: How much data is reserved for validation
        """

        print("_______________________________________________")
        print("--> Training model:\n\n")

        # if len(self.x_train.shape) == 3:
        #     if self.x_train.shape[1] == 1:
        #         batch_size = self.x_train.shape[1]
        #     else:
        #         batch_size = self.x_train.shape[0]

        self.history = self.model.fit(self.x_train, self.y_train,
                                      batch_size=batch_size,
                                      epochs=nb_epoch,
                                      shuffle=False,
                                      validation_split=validation_split,
                                      verbose=verbose)

        self.nb_epoch = nb_epoch

        print("-- Model fitted successfully --")
        return

    def evaluate_model(self, verbose=1):
        """
        Evaluate the model

        :param verbose: Specifies verbosity mode(0 = silent, 1= progress bar, 2 = one line per epoch)
        :return: Score
        """
        if self.history is not None:
            self.score = self.model.evaluate(self.x_test, self.y_test, verbose=verbose)

            print("\n\n_______________________________________________")
            print("Test score:", self.score[0])
            print("Test accuracy:", self.score[1])
            print("_______________________________________________")

        else:
            print(cf["red"]+"\n!!!!!Model needs to be fitted first to be evaluated!!!!!")
            sys.exit()
        return

    def plot_training_progress(self):
        """
        Generate plot of training progress (Training loss, validation loss)
        """
        if self.history is not None:

            history_dic = self.history.history
            epochs = range(1, self.nb_epoch + 1)

            plt.plot(epochs, history_dic["loss"], label="Training loss")
            plt.plot(epochs, history_dic["val_loss"], label="Validation loss")

            plt.title("Training and validation loss")
            plt.xlabel("Epochs")
            plt.ylabel("Loss")
            plt.legend()
            plt.show()

            plt.plot(epochs, history_dic["val_accuracy"], label="Validation accuracy")
            plt.plot(epochs, history_dic["accuracy"], label="Training accuracy")

            plt.title("Training and validation accuracy")
            plt.xlabel("Epochs")
            plt.ylabel("Accuracy")
            plt.legend()
            plt.show()

        else:
            print(cf["red"]+"\n!!!!!Model needs to be fitted first to obtain training progress!!!!!")
            sys.exit()
        return
