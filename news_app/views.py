from django.shortcuts import render
from .models import News, Category
from django.db.models import Q
from django.contrib import messages
from django.views.generic import TemplateView, DetailView
from pyfcm import FCMNotification
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pwa_webpush.models import Group



from django.core.paginator import Paginator

class HomeView(TemplateView):
    template_name = 'news_app/index.html'
    items_per_page = 8  # Number of items per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch the search query and queryset
        search_query = self.request.GET.get('q')
        queryset = News.objects.all() if not search_query else News.objects.filter(
            Q(title__icontains=search_query) | Q(brief__icontains=search_query)
        )
        
        # Paginate the queryset
        paginator = Paginator(queryset.order_by('-timestamp'), self.items_per_page)
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)
        
        context['news'] = page
        context['categories'] = Category.objects.all()
        context['trending_items'] = News.objects.order_by('-timestamp').first()
        context['search_query'] = search_query
        context['latest_news'] = News.objects.order_by('-timestamp')[:5]
        

        # Add code to send a push notification when a new news detail page is visited
        if self.request.user.is_authenticated:
            try:
                push_service = FCMNotification(api_key=settings.FIREBASE_WEB_API_KEY)
                registration_id = self.request.user.firebase_device_token  # Retrieve the user's Firebase device token
                message_title = "New Article!"
                message_body = f"A new article '{news.title}' has been published."
                result = push_service.notify_single_device(
                    registration_id=registration_id, message_title=message_title, message_body=message_body
                )
                print("Push notification result:", result)
            except Exception as e:
                print("Push notification error:", str(e))

        return context

    
class NewsDetailView(DetailView):
    model = News
    template_name = 'news_app/news_detail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch the search query and queryset
        search_query = self.request.GET.get('q')
        queryset = News.objects.all() if not search_query else News.objects.filter(
            Q(title__icontains=search_query) | Q(brief__icontains=search_query)
        )
        
        news = context['news']
        paginator = Paginator(queryset, 1)  # 1 post per page
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)
        
        context['search_query'] = search_query
        context['latest_news'] = News.objects.order_by('-timestamp')[:5]
        
        if page.has_previous():
            prev_page_number = page.previous_page_number()
            prev_post = paginator.page(prev_page_number).object_list.first()
            context['prev_post'] = prev_post
        
        if page.has_next():
            next_page_number = page.next_page_number()
            next_post = paginator.page(next_page_number).object_list.first()
            context['next_post'] = next_post
        
        return context

@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        subscription = request.POST.get('subscription')
        user = request.user  # or fetch the user from your context
        Group = get_group_model()
        group = Group.objects.get_or_create(name=str(user))[0]
        group.subscriptions.create(
            subscription_json=subscription,
            user=user
        )
        return JsonResponse({'message': 'Subscribed successfully.'})
    return JsonResponse({'message': 'Invalid request.'}, status=400)
