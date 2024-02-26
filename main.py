from ultralytics import YOLO

# load a model
model = YOLO("yolov8n.yaml")    # build a new model from scratch

# train the model for 300 epochs
results = model.train(data="signs-config.yaml", epochs=300)  #train the model

# Evaluate the model's performance on the validation set
results = model.val()

# Export the model to ONNX format
success = model.export(format='onnx')
