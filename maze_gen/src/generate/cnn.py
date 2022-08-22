import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, AveragePooling1D, Flatten, Concatenate
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USER = 'user4'
NUM_CLASSES = 5

class CNN:
    """Neural network model used to classify 1D sip and puff signals."""

    def __init__(self, num_classes=5):
        """Define and allocate layers.

        Args:
            num_classes (int, optional): Number of classes to predict. Defaults to 5.
        """

        self.net = Sequential()
        self.net.add(Conv1D(32, (11), activation='relu', input_shape=(150,1)))
        self.net.add(AveragePooling1D(pool_size=(5)))
        self.net.add(Conv1D(32, (5), activation='relu'))
        self.net.add(AveragePooling1D(pool_size=(3)))
        self.net.add(Conv1D(32, (3), activation='relu'))
        self.net.add(AveragePooling1D(pool_size=(3)))

        self.net.add(Flatten())

        self.net.add(Dense(512, activation='relu', kernel_initializer='glorot_uniform'))
        self.net.add(Dense(100, activation='relu', kernel_initializer='glorot_uniform'))
        self.net.add(Dense(20, activation='relu', kernel_initializer='glorot_uniform'))
        self.net.add(Dense(num_classes, activation='softmax', kernel_initializer='glorot_uniform'))
        

    def preprocess_data(self):
        """Read data from csv to use in model training and testing.

        Returns:
            data (pd.DataFrame): Dataframe containing sip and puff data from csv
        """

        data = pd.read_csv(f'{ROOT_DIR}/data/augmented_{USER}.csv')
        data = data.fillna(0)
        data = data.drop(['Unnamed: 0'], axis=1)
        return data

    def process_train_test(self, data):
        """Split data into train/test sets and process.

        Args:
            data (pd.DataFrame): Dataframe containing data to be split/processed

        Returns:
            ndarray: Processed data split randomly into train and test sets
        """
        y = data['labels']
        X = data.drop(['labels'], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.1)

        X_train = np.array(X_train)
        X_test = np.array(X_test)
        y_train = np.array(y_train)
        y_test = np.array(y_test)

        scaler = MinMaxScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        # Transform the target values
        y_train_cat = to_categorical(y_train)
        y_test_cat = to_categorical(y_test)

        #Add a dimension to each sequence
        X_train = np.array(X_train).reshape(X_train.shape[0], X_train.shape[1], 1)
        X_test = np.array(X_test).reshape(X_test.shape[0], X_test.shape[1], 1)

        return X_train, X_test, y_train, y_test, y_train_cat, y_test_cat

        
    def process_data(self, data, labels=False):
        new_data = []
        for i in range(len(data) - 149):
            slice = data[i:i+150]
            new_data.append(slice)

        if labels:
            new_data = [round(np.mean(x)) for x in new_data]

        return new_data

    def print_accuracy(self, X_test, y_test):
        # Get the predictions and convert the multicolumn array into class predictions.
        y_pred = np.argmax(self.net.predict(X_test), axis=1)

        # Plot the confusion matrix and print the final accuracy.
        cnn_cm = confusion_matrix(y_pred, y_test)
        cnn_cm_disp = ConfusionMatrixDisplay(confusion_matrix=cnn_cm)

        cnn_cm_disp.plot()
        cnn_cm_disp.ax_.set_title('CNN Confusion Matrix')
        plt.show()

        print('Accuracy:', accuracy_score(y_pred, y_test))

def main():
    cnn = CNN()

    data = cnn.preprocess_data()

    X_train, X_test, y_train, y_test, y_train_cat, y_test_cat = cnn.process_train_test(data)

    cnn.net.compile(optimizer='adam', loss='binary_crossentropy', metrics = ['accuracy'])
    early = EarlyStopping(monitor='val_loss', patience=3)
    cnn_history = cnn.net.fit(X_train, y_train_cat, validation_split=0.1, epochs=10, callbacks=[early])

    cnn.print_accuracy(X_test, y_test)

if __name__ == '__main__':
    main()
    

    
