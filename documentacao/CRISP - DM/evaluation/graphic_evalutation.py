from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

def plot_roc_cure(models : dict, X: list, y: list):

    for name, model in models.items():
        if name == "LR" or name == "XGB":
            y_prob = model.predict_proba(X[0])[:,1]
            fpr, tpr, _ = roc_curve(y[0], y_prob)
        else:
            y_prob = model.predict_proba(X[1])[:,1]
            fpr, tpr, _ = roc_curve(y[1], y_prob)

    plt.plot(fpr, tpr, label=name)

    plt.plot([0,1], [0,1], '--')
    plt.legend()
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.title('Curva ROC - Validação')
   