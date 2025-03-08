import os
import joblib
from django.shortcuts import render
from django.http import JsonResponse

# Get the absolute path of the model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'news_classifier.pkl')

# Load the model safely
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None
    print("Error: Model file not found. Ensure 'news_classifier.pkl' exists.")
    
    
def home(request):
    return render(request, 'index.html')

# views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
def predict_news(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        if model:
            # Get the prediction and the probabilities
            prediction = model.predict([text])[0]
            probabilities = model.predict_proba([text])[0]
            
            # Determine if the news is real or fake
            result = "Fake" if prediction == 1 else "Real"
            
            # Generate a reason based on the prediction and probabilities
            if prediction == 1:
                reason = f"The model is {probabilities[1] * 100:.2f}% confident that this news is fake. It may contain sensational or misleading information."
            else:
                reason = f"The model is {probabilities[0] * 100:.2f}% confident that this news is real. It appears to be credible and well-sourced."
            
            # Include whether the user is authenticated in the response
            response_data = {
                'result': result,
                'reason': reason,
                'authenticated': request.user.is_authenticated,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': "Model not found"}, status=500)
    return render(request, 'dectector.html')
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from .models import NewsArticle
import json

@method_decorator(csrf_exempt, name='dispatch')
class ClassifyNewsView(View):
    def post(self, request, *args, **kwargs):
        """Handle news submission via POST request."""
        try:
            data = json.loads(request.body)  # Parse JSON request body
            title = data.get("title", "")
            text = data.get("text", "")
            subject = data.get("subject", "")
            date = data.get("date", None)

            if not text:
                return JsonResponse({"error": "Text field is required"}, status=400)

            # Create and classify news (classification is automatic now)
            article = NewsArticle.objects.create(
                title=title,
                text=text,
                subject=subject,
                date=date
            )

            return JsonResponse({
                "message": "News classified successfully",
                "is_fake": article.is_fake,
                "id": article.id
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
