import pandas as pd
from math import *


class Confusion_matrix_analysis:
    def __init__(self, model_predictions, metalabels, print_benchmark_results=False):

        self.model_predictions = model_predictions
        self.metalabels = metalabels

        # ------------------------------------------------- Confusion matrix
        cm_init = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        """Confusion_matrix columns = Metalabels, rows = Prediction"""
        # confusion_matrix = pd.DataFrame(init, columns=[1, 0, -1], index=[1, 0, -1])
        confusion_matrix = pd.DataFrame(cm_init, columns=["Sell", "Hold", "Buy"], index=["Sell", "Hold", "Buy"])

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

        self.confusion_matrix = confusion_matrix

        # ------------------------------------------------- Confusion tables
        ct_init = [["", ""], ["", ""]]
        # ---> Reference table
        self.confusion_table_ref = pd.DataFrame(ct_init, columns=["Condition Positive 0", "Condition Negative 1"],
                                                index=["Predicted Condition Positive 0", "Predicted Condition Negative 1"])
        # True positive
        self.confusion_table_ref.at['Predicted Condition Positive', 'Condition Positive'] = 'True positive'
        # True negative
        self.confusion_table_ref.at['Predicted Condition Negative', 'Condition Negative'] = 'True negative'
        # False Positive
        self.confusion_table_ref.at['Predicted Condition Positive', 'Condition Negative'] = 'False positive'
        # False Negative
        self.confusion_table_ref.at['Predicted Condition Negative', 'Condition Positive'] = 'False Negative'

        ct_init = [[0, 0], [0, 0]]

        # ---> Sell
        self.confusion_table_sell = pd.DataFrame(ct_init, columns=["Sell", "Non-Sell"], index=["Sell", "Non-Sell"])

        # True Positive
        self.confusion_table_sell.at['Sell', 'Sell'] = confusion_matrix.at['Sell', 'Sell']
        # True Negative
        self.confusion_table_sell.at['Non-Sell', 'Non-Sell'] = confusion_matrix.at['Hold', 'Hold'] + \
                                                               confusion_matrix.at['Buy', 'Buy'] + \
                                                               confusion_matrix.at['Hold', 'Buy'] + \
                                                               confusion_matrix.at['Buy', 'Hold']
        # False Positive
        self.confusion_table_sell.at['Sell', 'Non-Sell'] = confusion_matrix.at['Sell', 'Hold'] + \
                                                           confusion_matrix.at['Sell', 'Buy']

        # False Negative
        self.confusion_table_sell.at['Non-Sell', 'Sell'] = confusion_matrix.at['Hold', 'Sell'] + \
                                                           confusion_matrix.at['Buy', 'Sell']

        # ---> Buy
        self.confusion_table_buy = pd.DataFrame(ct_init, columns=["Buy", "Non-Buy"], index=["Buy", "Non-Buy"])

        # True Positive
        self.confusion_table_buy.at['Buy', 'Buy'] = confusion_matrix.at['Buy', 'Buy']
        # True Negative
        self.confusion_table_buy.at['Non-Buy', 'Non-Buy'] = confusion_matrix.at['Hold', 'Hold'] + \
                                                             confusion_matrix.at['Sell', 'Sell'] + \
                                                             confusion_matrix.at['Hold', 'Sell'] + \
                                                             confusion_matrix.at['Sell', 'Hold']
        # False Positive
        self.confusion_table_buy.at['Buy', 'Non-Buy'] = confusion_matrix.at['Buy', 'Hold'] + \
                                                         confusion_matrix.at['Buy', 'Sell']

        # False Negative
        self.confusion_table_buy.at['Non-Buy', 'Buy'] = confusion_matrix.at['Hold', 'Buy'] + \
                                                         confusion_matrix.at['Sell', 'Buy']

        # ---> Hold
        self.confusion_table_hold = pd.DataFrame(ct_init, columns=["Hold", "Non-Hold"], index=["Hold", "Non-Hold"])

        # True Positive
        self.confusion_table_hold.at['Hold', 'Hold'] = confusion_matrix.at['Hold', 'Hold']
        # True Negative
        self.confusion_table_hold.at['Non-Hold', 'Non-Hold'] = confusion_matrix.at['Sell', 'Sell'] + \
                                                               confusion_matrix.at['Buy', 'Buy'] + \
                                                               confusion_matrix.at['Sell', 'Buy'] + \
                                                               confusion_matrix.at['Buy', 'Sell']
        # False Positive
        self.confusion_table_hold.at['Hold', 'Non-Hold'] = confusion_matrix.at['Hold', 'Sell'] + \
                                                           confusion_matrix.at['Hold', 'Buy']

        # False Negative
        self.confusion_table_hold.at['Non-Hold', 'Hold'] = confusion_matrix.at['Sell', 'Hold'] + \
                                                           confusion_matrix.at['Buy', 'Hold']

        # ------------------------------------------------- Accuracy calculations
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

        if print_benchmark_results:
            print("Overall accuracy achieved:", round(self.overall_accuracy))
            print("Overall accuracy achieved (excluding hold):", round(self.overall_accuracy_bs))
            print("\nConfusion matrix:\n", confusion_matrix, "\n")

    @staticmethod
    def calc_TPR(cm):
        tp = cm.ix[0, 0]
        fn = cm.ix[1, 0]

        return tp/(tp+fn)

    @staticmethod
    def calc_TNR(cm):
        tn = cm.ix[1, 1]
        fp = cm.ix[0, 1]
        return tn/(tn+fp)

    @staticmethod
    def calc_PPV(cm):
        tp = cm.ix[0, 0]
        fp = cm.ix[0, 1]
        return tp/(tp+fp)

    @staticmethod
    def calc_NPV(cm):
        tn = cm.ix[1, 1]
        fn = cm.ix[1, 0]
        return tn/(tn+fn)

    @staticmethod
    def calc_FNR(cm):
        tp = cm.ix[0, 0]
        fn = cm.ix[1, 0]
        return fn/(fn+tp)

    @staticmethod
    def calc_FPR(cm):
        tn = cm.ix[1, 1]
        fp = cm.ix[0, 1]
        return fp/(fp+tn)

    @staticmethod
    def calc_FDR(cm):
        tp = cm.ix[0, 0]
        fp = cm.ix[0, 1]
        return fp/(fp+tp)

    @staticmethod
    def calc_FOR(cm):
        tn = cm.ix[1, 1]
        fn = cm.ix[1, 0]
        return fn/(fn+tn)

    @staticmethod
    def calc_ACC(cm):
        tp = cm.ix[0, 0]
        tn = cm.ix[1, 1]
        fp = cm.ix[0, 1]
        fn = cm.ix[1, 0]
        return (tp+tn)/(tp+tn+fp+fn)

    @staticmethod
    def calc_F1(cm):
        tp = cm.ix[0, 0]
        fp = cm.ix[0, 1]
        fn = cm.ix[1, 0]
        return 2*tp/(2*tp+fp+fn)

    @staticmethod
    def calc_MCC(cm):
        tp = cm.ix[0, 0]
        tn = cm.ix[1, 1]
        fp = cm.ix[0, 1]
        fn = cm.ix[1, 0]
        return (tp*tn-fp*fn)/(sqrt((tp+fp)(tp+fn)(tn+fp)(tn+fn)))

    @staticmethod
    def calc_BM(cm):
        tp = cm.ix[0, 0]
        tn = cm.ix[1, 1]
        fp = cm.ix[0, 1]
        fn = cm.ix[1, 0]
        return tp/(tp+fn) + tn/(tn+fp) - 1

    @staticmethod
    def calc_MK(cm):
        tp = cm.ix[0, 0]
        tn = cm.ix[1, 1]
        fp = cm.ix[0, 1]
        fn = cm.ix[1, 0]
        return tp/(tp+fp) + tn/(tn+fn) - 1