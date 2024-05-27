from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    PostByCategoryView,
    PostByTagView,
    SearchResultsListView,
)

urlpatterns = [
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path("new/", BlogCreateView.as_view(), name="post_new"),
    path("<slug:slug>/", BlogDetailView.as_view(), name="post_detail"),
    path("<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"),
    path("<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),
    path("category/<slug:category_slug>/", PostByCategoryView.as_view(), name='category'),
    path("tag/<slug:tag_slug>/", PostByTagView.as_view(), name='tag'),
    path("", BlogListView.as_view(), name="post_list"),
]
