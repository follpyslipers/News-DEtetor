import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

# Load datasets
df_fake = pd.read_csv('fake.csv')
df_true = pd.read_csv('true.csv')

# Assign labels
df_fake['label'] = 1  # Fake news
df_true['label'] = 0  # True news

# Ensure column names are correct
print("Fake news columns:", df_fake.columns)
print("True news columns:", df_true.columns)

# Check if 'text' column exists
df_fake.rename(columns={'Text': 'text'}, inplace=True)
df_true.rename(columns={'Text': 'text'}, inplace=True)

# Combine datasets
df = pd.concat([df_fake, df_true], ignore_index=True)

# Shuffle data
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Check the structure of the dataframe
print("Dataset columns:", df.columns)
print(df.head())

# Ensure 'text' and 'label' columns exist
if 'text' not in df.columns or 'label' not in df.columns:
    raise KeyError("Required columns 'text' and 'label' are missing in the dataset.")

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# Create a text classification pipeline
model = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', MultinomialNB())
])

# Train the model
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f}")
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, 'news_classifier.pkl')
print("Model training complete. Saved as 'news_classifier.pkl'.")