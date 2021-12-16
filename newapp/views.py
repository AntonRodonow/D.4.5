from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm

class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 3
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):   # добавил +
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)

class PostDetailView(DetailView):               # работает дженерик для деталей новостей
    template_name = 'newapp/post_detail.html'
    queryset = Post.objects.all()
    context_object_name = 'new'

class PostAddView(CreateView):              # работает дженерик создания новостей
    template_name = 'newapp/post_add.html'
    form_class = PostForm

class PostDetail(DetailView):          # скорее всего уже не понадобится
    model = Post
    template_name = 'post.html'
    context_object_name = 'new'

class PostListFilter(ListView):
    model = Post
    template_name = 'postsfilter.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        # context['categories'] = Category.objects.all()
        # context['form'] = PostForm()
        return context

class PostUpdateView(UpdateView):               # дженерик для редактирования новостей
    template_name = 'newapp/post_add.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):            # дженерик для удаления новостей
    template_name = 'newapp/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
