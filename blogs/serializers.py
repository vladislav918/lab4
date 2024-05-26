from rest_framework import serializers
from.models import Post, Tag, Category, Comment
from django.contrib.auth import get_user_model


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'id']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body', 'id']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'id']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tag = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = ['name', 'description', 'featured_image', 'slug', 'author', 'tag', 'category', 'comments']


    def get_comments(self, obj):
        request = self.context.get('request')
        include_comments = request.query_params.get('include', '').lower() == 'comments'
        
        if include_comments:
            comments = Comment.objects.filter(post=obj)
            serializer = CommentSerializer(comments, many=True)
            return serializer.data
        
        return None


class PostCreateSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Post
        exclude = ['featured_image', 'slug']
   

