import tensorflow

model = tensorflow.keras.saving.load_model("model/RADAR_F1_93")
model.summary()