from sklearn.metrics import fbeta_score, precision_score, recall_score
from xgboost import XGBClassifier
from ml.data import process_data
import json


# Optional: implement hyperparameter tuning.
def train_model(X_train, y_train):
    """
    Trains a machine learning model and returns it.

    Inputs
    ------
    X_train : np.array
        Training data.
    y_train : np.array
        Labels.
    Returns
    -------
    model
        Trained machine learning model.
    """

    xgb = XGBClassifier()

    xgb.fit(X_train,y_train)

    return xgb



def compute_model_metrics(y, preds):
    """
    Validates the trained machine learning model using precision, recall, and F1.

    Inputs
    ------
    y : np.array
        Known labels, binarized.
    preds : np.array
        Predicted labels, binarized.
    Returns
    -------
    precision : float
    recall : float
    fbeta : float
    """
    fbeta = fbeta_score(y, preds, beta=1, zero_division=1)
    precision = precision_score(y, preds, zero_division=1)
    recall = recall_score(y, preds, zero_division=1)
    return precision, recall, fbeta


def inference(model, X):
    """ Run model inferences and return the predictions.

    Inputs
    ------
    model : XGBClassifier
        Trained machine learning model.
    X : np.array
        Data used for prediction.
    Returns
    -------
    preds : np.array
        Predictions from the model.
    """

    X = process_data(X)
    return model.predict(X)


def slices_performance(X, y, fixes, model):

    cat_ft = json.load(open('../data/cat_ft.json'))

    for col in cat_ft:
        fixes[col] = {}
        for slice in X.columns[X.columns.str.contains(col+'_')]:

            fixes[col][slice] = {}

            temp = X[X[slice]==1]
            y_t = y[temp.index]

            y_pred = model.predict(temp)

            metrics = compute_model_metrics(y_t,y_pred)

            fixes[col][slice]['precision'] = metrics[0]
            fixes[col][slice]['recall'] = metrics[1]
            fixes[col][slice]['f1'] = metrics[2]

    return fixes
    
