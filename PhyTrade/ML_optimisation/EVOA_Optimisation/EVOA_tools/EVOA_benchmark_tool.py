import pandas as pd


class Confusion_matrix_analysis:
    def __init__(self, model_predictions, metalabels, print_benchmark_results=False):

        self.model_predictions = model_predictions
        self.metalabels = metalabels

        # ------------------ Confusion matrix
        init = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        # confusion_matrix = pd.DataFrame(init, columns=[1, 0, -1], index=[1, 0, -1])
        confusion_matrix = pd.DataFrame(init, columns=["Sell", "Hold", "Buy"], index=["Sell", "Hold", "Buy"])

        for i in range(len(model_predictions)):
            if model_predictions[i] == metalabels[i]:
                if model_predictions[i] == 1:
                    confusion_matrix.at['Sell', 'Sell'] += 1
                elif model_predictions[i] == -1:
                    confusion_matrix.at['Buy', 'Buy'] += 1
                else:
                    confusion_matrix.at['Hold', 'Hold'] += 1

            else:
                if model_predictions[i] == 0 and metalabels[i] == 1:
                    confusion_matrix.at['Hold', 'Sell'] += 1

                elif model_predictions[i] == -1 and metalabels[i] == 1:
                    confusion_matrix.at['Buy', 'Sell'] += 1

                elif model_predictions[i] == 1 and metalabels[i] == 0:
                    confusion_matrix.at['Sell', 'Hold'] += 1

                elif model_predictions[i] == -1 and metalabels[i] == 0:
                    confusion_matrix.at['Buy', 'Hold'] += 1

                elif model_predictions[i] == 1 and metalabels[i] == -1:
                    confusion_matrix.at['Sell', 'Buy'] += 1

                elif model_predictions[i] == 0 and metalabels[i] == -1:
                    confusion_matrix.at['Hold', 'Buy'] += 1

        # ------------------ Confusion table
        # True positive count:
        tp_count = 0
        # True negative count:
        tn_count = 0

        # False positive count:
        fp_count = 0
        # False negative count:
        fn_count = 0

        # ------------------ Accuracy calculations
        # -- Overall accuracy
        correct_prediction = 0
        wrong_prediction = 0

        correct_prediction_bs = 0
        wrong_prediction_bs = 0

        for i in range(len(self.model_predictions)):
            if self.model_predictions[i] == self.metalabels[i]:
                correct_prediction += 1

                if self.model_predictions[i] == 1 or self.model_predictions[i] == -1:
                    correct_prediction_bs += 1

            else:
                wrong_prediction += 1

                if self.model_predictions[i] == 1 or self.model_predictions[i] == -1:
                    wrong_prediction_bs += 1

        self.overall_accuracy = correct_prediction / len(self.model_predictions) * 100
        self.overall_accuracy_bs = correct_prediction_bs / (correct_prediction_bs + wrong_prediction_bs) * 100

        # -- Confusion matrix accuracy
        self.ACC = (confusion_matrix.at['Sell', 'Sell'] + confusion_matrix.at['Buy', 'Buy']) / \
                   (confusion_matrix.at['Sell', 'Sell'] + confusion_matrix.at['Buy', 'Buy'] +
                    (confusion_matrix.at['Sell', 'Buy'] + confusion_matrix.at['Buy', 'Sell']))

        # print(self.ACC)

        if print_benchmark_results:
            print("Overall accuracy achieved:", round(self.overall_accuracy))
            print("Overall accuracy achieved (excluding hold):", round(self.overall_accuracy_bs))
            print("\nConfusion matrix:\n", confusion_matrix, "\n")

        # init = {"Metalabels": self.metalabels, "Model Predictions": self.model_predictions}
        # df = pd.DataFrame(data=init)
        # print(df)
