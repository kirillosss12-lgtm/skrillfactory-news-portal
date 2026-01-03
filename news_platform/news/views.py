from django.shortcuts import render, get_object_or_404
from  .models import Tovar


# Create your views here.
def index(request):
    all_news = Tovar.objects.order_by('-data')[:3]
    context={
        'main_post': all_news[0] if all_news else None,
        'side_news': all_news[1:3]
    }
    return render(request, 'index.html', context)

def news(request):
    post = Tovar.objects.all()
    context = {'post' : post}
    return render(request, 'news.html', context=context)


def news_detail(request ,pk):
    article = get_object_or_404(Tovar, pk=pk)
    return render(request, 'news_detail.html', {'article': article})