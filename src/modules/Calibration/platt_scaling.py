from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator


def platt_scaling(model, X_cal, y_cal, X_test):

    print("\n-----PLATT SCALING-----")

    frozen_model = FrozenEstimator(model)
    calibrated_model = CalibratedClassifierCV(estimator=frozen_model, method="sigmoid")

    # Fit calibration trên calibration set
    calibrated_model.fit(X_cal, y_cal)

    # Probability sau calibration
    y_prob_platt = calibrated_model.predict_proba(X_test)[:, 1]
    y_pred_platt = calibrated_model.predict(X_test)

    return calibrated_model, y_prob_platt, y_pred_platt
