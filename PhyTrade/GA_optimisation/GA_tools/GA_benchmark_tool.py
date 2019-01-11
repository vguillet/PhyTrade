import pandas as pd


class Confusion_matrix_analysis:
    def __init__(self, model_predictions, metalabels):

        self.model_predictions = model_predictions
        self.metalabels = metalabels

        # init = {"Metalabels": self.metalabels, "Model Predictions": self.model_predictions}
        # df = pd.DataFrame(data=init)
        # print(df)


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

        print("Confusion matrix:\n", confusion_matrix, "\n")
        # ------------------ Confusion table
        # True positive count:
        tp_count = 0
        # True negative count:
        tn_count = 0

        # False positive count:
        fp_count = 0
        # False negative count:
        fn_count = 0
