from django.http import HttpResponse
from .models import Article

def article_list(request):
    articles = Article.objects.filter(tenant=request.tenant)
    return HttpResponse(", ".join(article.title for article in articles))
