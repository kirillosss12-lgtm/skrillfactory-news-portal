from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from .models import Tovar, Category


@shared_task
def send_notifications(post_id):
    """Рассылка сразу после создания новости"""
    post = Tovar.objects.get(pk=post_id)
    categories = post.category.all()
    subscribers_emails = set()

    for cat in categories:
        subscribers_emails.update(cat.subscribers.values_list('email', flat=True))

    for email in subscribers_emails:
        html_content = render_to_string('post_created_email.html', {'post': post})
        msg = EmailMultiAlternatives(
            subject=post.title,
            body=post.text[:50],
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def weekly_newsletter():
    """Рассылка по понедельникам"""
    last_week = timezone.now() - timedelta(days=7)
    posts = Tovar.objects.filter(time_in__gte=last_week)
    categories = Category.objects.all()

    for category in categories:
        cat_posts = posts.filter(category=category)
        if cat_posts.exists():
            emails = category.subscribers.values_list('email', flat=True)
            if emails:
                html_content = render_to_string(
                    'weekly_digest.html',
                    {'posts': cat_posts, 'category': category, 'link': settings.SITE_URL}
                )
                msg = EmailMultiAlternatives(
                    subject=f'Новости за неделю: {category.name}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=emails,
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()