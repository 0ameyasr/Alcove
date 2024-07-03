import pandas, numpy, tensorflow
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

dataset = pandas.read_csv("data/radar.csv")
X = numpy.array(dataset[["PHQ","GAD","BDI","PSQI","AFI"]])
y = numpy.array(dataset[["NONE","MILD","MOD","SEV"]])
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.20)

scaler = StandardScaler()
scX_train = scaler.fit_transform(X_train)
scX_test = scaler.transform(X_test)

ANN = tensorflow.keras.models.Sequential([
    Dense(8,activation='relu'),
    Dense(16,activation='relu'),
    Dense(4,activation='softmax')
])
ANN.compile(optimizer="adam",loss='categorical_crossentropy',metrics=['accuracy'])

ANN.fit(scX_train,y_train,epochs=1000,validation_split=0.2)