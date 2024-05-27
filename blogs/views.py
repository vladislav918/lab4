from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import Q


from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm, PostUpdateForm


# class AuthorRequiredMixin:
#     def get_object(self):
#         post = get_object_or_404(Post, pk=self.kwargs['pk'])
#         if post.author == self.request.user:
#             return post
#         else:
#             raise PermissionDenied


# class SearchResultsListView(ListView):
#     model = Post
#     template_name = 'post/post_list_by_search.html'


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         categories = Category.objects.all()
#         context['categories'] = categories
#         return context

#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         category_id = self.request.GET.get('category')
#         if category_id:
#             return Post.objects.filter(Q(name__icontains=query) & Q(category_id=category_id))
#         else:
#             return Post.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))


# class BlogListView(ListView):
#     model = Post
#     paginate_by = 2
#     template_name = "post/post_list.html"
#     queryset = Post.objects.all().select_related('author').select_related('category').prefetch_related('tag')


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         category = Category.objects.all()
#         context['categories'] = category
#         tag = Tag.objects.all()
#         context['tags'] = tag
#         return context


# class BlogDetailView(DetailView):
#     model = Post
#     template_name = "post/post_detail.html"
#     queryset = Post.objects.all().select_related('author')


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.object
#         comments = Comment.objects.filter(post=post).select_related('author')
#         context['comments'] = comments
#         context['form'] = CommentForm()
#         return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.post = self.object
#             comment.save()
#             return redirect('post_detail', slug=self.object.slug)
#         return self.render_to_response(self.get_context_data(form=form))


# class BlogCreateView(SuccessMessageMixin, CreateView):
#     model = Post
#     template_name = "post/post_new.html"
#     form_class = PostForm
#     success_message = "%(name)s успешно создан"
#     success_url = reverse_lazy('post_list')

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


# class BlogUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = Post
#     template_name = "post/post_edit.html"
#     form_class = PostUpdateForm
#     success_message = "%(name)s успешно обновлен"


# class BlogDeleteView(AuthorRequiredMixin, DeleteView):
#     model = Post
#     template_name = "post/post_delete.html"
#     success_url = reverse_lazy("post_list")


# class PostByCategoryView(ListView):
#     model = Post
#     template_name = 'post/post_list_by_category.html'

#     def get_queryset(self):
#         print(self.kwargs['category_slug'])
#         return Post.objects.filter(category__slug=self.kwargs['category_slug'])


# class PostByTagView(ListView):
#     model = Post
#     template_name = 'post/post_list_by_tag.html'

#     def get_queryset(self):
#         print(self.kwargs['tag_slug'])
#         return Post.objects.filter(tag__slug=self.kwargs['tag_slug'])


# def handle_404(request, exception):
#     return render(request, '404.html', status=404)


from.models import Post, Comment
from.serializers import PostSerializer, CommentSerializer, PostCreateSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from .filters import PostFilter
from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView


class PostList(ListAPIView):
    serializer_class = PostSerializer
    filterset_class = PostFilter

    def get_queryset(self):
        queryset = Post.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(author__username=username)
        
        print(queryset)  
        
        return queryset



@api_view(['GET'])
def post_comments(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)

    comments = Comment.objects.filter(post=post)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_post(request):
    serializer = PostCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class PostCreate(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    
    


#'{"name": "My New Post", "description": "This is my first post.", "author": 1, "tag": [1, 2], "category": 1}'