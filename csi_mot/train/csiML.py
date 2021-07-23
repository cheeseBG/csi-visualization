import logging
import pandas as pd
import csi_mot.train.data.generateDB as db
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

# Create Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - ' + '\n' + '%(message)s')

# Set log stream handler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Set log file handler
file_handler = logging.FileHandler('./log/' + str(db.file_name) + '.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

data_filename = 'sub' + str(db.file_name) + '.xlsx'
data_filepath = '/'.join(['data', data_filename])

# Read data file and create dataframe
try:
    df = pd.read_excel(data_filepath)

    # # Read another dataset for test
    # test_df = pd.read_excel('/'.join(['data', 'sub3[14, 15].xlsx']))
except FileNotFoundError:
    print(f'File {data_filepath} not found.')
    exit(-1)

# Delete row index in dataframe
del df['Unnamed: 0']
# del test_df['Unnamed: 0']

# Min-Max Normalization
scaler = MinMaxScaler()
scaler.fit(df.iloc[:, 0:100])
scaled_df = scaler.transform(df.iloc[:, 0:100])
df.iloc[:, 0:100] = scaled_df

# # Min-Max Normalization for test data
# scaler = MinMaxScaler()
# scaler.fit(test_df.iloc[:, 0:100])
# scaled_df = scaler.transform(test_df.iloc[:, 0:100])
# test_df.iloc[:, 0:100] = scaled_df


def roc_curve_plot(model_name, fpr, tpr, roc_auc):
    plt.plot(fpr, tpr, linewidth=2, label='Area(AUC) = %0.2f' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.axis([0, 1, 0, 1])
    plt.title(model_name + ' ROC Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc="lower right")

    plt.show()


# # Split train, test data with different dataset
# train_feature = df.drop(columns=['label'])
# train_target = df['label']
#
# test_feature = test_df.drop(columns=['label'])
# test_target = test_df['label']

# Split dataset
train_data, test_data = train_test_split(df, test_size=0.3)
train_feature = train_data.drop(columns=['label'])
train_target = train_data['label']

test_feature = test_data.drop(columns=['label'])
test_target = test_data['label']

# K-fold validation (k = 10)
kf = KFold(n_splits=10, shuffle=True)

# Set parameter list
param = {'C': [0.1, 1.0],
         'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
         'gamma': [0.01, 0.1, 1.0]}

svm = SVC(probability=True)

# Set Grid Search
grid_search = GridSearchCV(estimator=svm, param_grid=param,
                           cv=kf, n_jobs=4, verbose=2)

# Fit the model
grid_search.fit(train_feature, train_target)

print("Best parameters: " + str(grid_search.best_params_))
print("Best score: " + str(grid_search.best_score_))

best_param = "Best parameters: " + str(grid_search.best_params_)

# Predict with test data
pred = grid_search.best_estimator_.predict(test_feature)
print(pred)

# Get ROC accuracy score
probs = grid_search.best_estimator_.predict_proba(test_feature)
print('#prob')
print(probs)
preds = probs[:, 1]
fpr, tpr, threshold = roc_curve(test_target, preds)
roc_auc = auc(fpr, tpr)

# Show ROC curve plot
#roc_curve_plot('SVM', fpr, tpr, roc_auc)

# Display confusion matrix
print("\n\n< SVM Confusion matrix >")
print(confusion_matrix(test_target, pred))
print(classification_report(test_target, pred))

logger.info('subcarriers: ' + str(db.file_name))
logger.info(best_param)
logger.info(confusion_matrix(test_target, pred))
logger.info(classification_report(test_target, pred))





