from django.db import models
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class NewsArticle(models.Model):
    title = models.CharField(max_length=5000)
    text = models.TextField()
    subject = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    is_fake = models.BooleanField(null=True, blank=True)  # Will be auto-classified

    model_path = os.path.join(BASE_DIR, 'news_classifier.pkl')

    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        model = None

    def classify_news(self):
        """Classify the article using the machine learning model."""
        if NewsArticle.model:
            prediction = NewsArticle.model.predict([self.text])[0]
            self.is_fake = bool(prediction)  # True if fake, False if real

    def save(self, *args, **kwargs):
        """Automatically classify the news before saving."""
        if self.is_fake is None:  # Only classify if not already set
            self.classify_news()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {'Fake' if self.is_fake else 'Real'}"
