import joblib

model = joblib.load('ml/model.joblib')
mlb = joblib.load('ml/label_binarizer.joblib')

def predict_roles(text):
    pred = model.predict([text])
    labels = mlb.inverse_transform(pred)

    if not labels[0]:  # If empty
        return ["Could not confidently predict a role"]
    return labels[0]

