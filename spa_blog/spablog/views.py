from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from .models import Post
from .forms import SignUpForm, SignInForm, ContactForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from taggit.models import Tag

Post.objects.all()


class MainView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'spablog/home.html', context={'page_object': page_object})


class PostDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        return render(request, 'spablog/post_detail.html', context={'post': post})


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'spablog/signup.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'spablog/signup.html', context={
            'form': form,
        })


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'spablog/signin.html', context={
            'form': form, })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'spablog/signin.html', context={'form': form, })


class ContactFormView(View):

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, 'spablog/contact.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_mail = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'Письмо от {name}. Тема {subject}', message, from_mail, ['lostdevil95@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Ошибка')
            return HttpResponseRedirect('success')
        return render(request, 'spablog/contact.html', context={
            'form': form,
        })


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'spablog/success.html')


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        result = ''
        if query:
            result = Post.objects.filter(Q(h1__icontains=query) | Q(content__icontains=query))
        paginator = Paginator(result, 8)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'spablog/search.html', context={'result': page_object, 'count': paginator.count})


class TagView(View):
    def get_page(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        post = Post.objects.filter(tag=tag)
        common_tags = Post.tag.most_common()
        return render(request, 'spablog/tag.html', context={'title': f'#ТЕГ {tag}',
                                                            'posts': post,
                                                            'common_tags': common_tags})
