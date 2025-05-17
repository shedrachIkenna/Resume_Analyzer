import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
import joblib

# Load data
df = pd.read_csv(r'C:\Users\DELL\Desktop\smart_resume_analyser\ml\data\resume.csv')
df['labels'] = df['labels'].apply(lambda x: x.split(','))

# Convert labels to binary
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(df['labels'])

# Vectorize + train
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', OneVsRestClassifier(LogisticRegression(solver='liblinear')))
])

pipeline.fit(df['text'], y)

# Save model and label binarizer
joblib.dump(pipeline, 'ml/model.joblib')
joblib.dump(mlb, 'ml/label_binarizer.joblib')

print("✅ Model trained and saved.")
