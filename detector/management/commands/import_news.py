import os
import pandas as pd
from django.core.management.base import BaseCommand
from detector.models import NewsArticle
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, 'news_classifier.pkl')

class Command(BaseCommand):
    help = "Import news articles from CSV files and classify them"

    def add_arguments(self, parser):
        parser.add_argument('fake_csv', type=str, help="Path to the fake news CSV file")
        parser.add_argument('true_csv', type=str, help="Path to the true news CSV file")

    def handle(self, *args, **kwargs):
        fake_csv_path = kwargs['fake_csv']
        true_csv_path = kwargs['true_csv']

        if not os.path.exists(fake_csv_path) or not os.path.exists(true_csv_path):
            self.stdout.write(self.style.ERROR("One or both CSV files do not exist."))
            return

        # Load datasets
        df_fake = pd.read_csv(fake_csv_path)
        df_true = pd.read_csv(true_csv_path)

        # Assign labels
        df_fake['label'] = True  # Fake news
        df_true['label'] = False  # Real news

        # Standardize column names
        rename_map = {'Text': 'text', 'Title': 'title', 'Subject': 'subject', 'Date': 'date'}
        df_fake.rename(columns=rename_map, inplace=True)
        df_true.rename(columns=rename_map, inplace=True)

        # Combine datasets
        df = pd.concat([df_fake, df_true], ignore_index=True)

        # Convert date column to proper format
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])  # Remove rows with NaT in the date column

        # Load the model for classification
        try:
            model = joblib.load(MODEL_PATH)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("Model file not found. Cannot classify news."))
            return

        articles = []
        for _, row in df.iterrows():
            # Check for duplicates by title
            if not NewsArticle.objects.filter(title=row['title']).exists():
                is_fake = bool(model.predict([row['text']])[0])  # Classify using model
                article = NewsArticle(
                    title=row['title'],
                    text=row['text'],
                    subject=row['subject'],
                    date=row['date'],
                    is_fake=is_fake  # Set classification directly
                )
                articles.append(article)

        if articles:
            NewsArticle.objects.bulk_create(articles)
            self.stdout.write(self.style.SUCCESS(f"Successfully imported and classified {len(articles)} articles!"))
        else:
            self.stdout.write(self.style.WARNING("No new articles found for import."))
