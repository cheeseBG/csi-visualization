import pandas as pd
import tensorflow as tf
import csi_mot.train.data.generateDB as db
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

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

# # Split train, test data with different dataset
# train_feature = df.drop(columns=['label'])
# train_target = df['label']
#
# test_feature = test_df.drop(columns=['label'])
# test_target = test_df['label']


# Split dataset
train_data, test_data = train_test_split(df, test_size=0.3)

train_feature = train_data.drop(columns=['label'])
train_target = tf.keras.utils.to_categorical(train_data['label'], num_classes=2)

test_feature = test_data.drop(columns=['label'])
test_target = tf.keras.utils.to_categorical(test_data['label'], num_classes=2)

print(train_feature.shape)
print(train_target.shape)

model = tf.keras.Sequential([tf.keras.layers.Dense(units=192, activation='relu', input_shape=(100,)),
                            tf.keras.layers.Dense(units=96, activation='relu'),
                            tf.keras.layers.Dense(units=48, activation='relu'),
                            tf.keras.layers.Dense(units=24, activation='relu'),
                            tf.keras.layers.Dense(units=12, activation='relu'),
                            tf.keras.layers.Dense(units=2, activation='sigmoid')])

model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.0001), loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

history = model.fit(train_feature, train_target, epochs=50, batch_size=25, validation_split=0.25, callbacks=[tf.keras.callbacks.EarlyStopping(patience=3, monitor='val_loss')])


print("\n Training is done! \n")

print("Evaluation:")
model.evaluate(test_feature, test_target)