from rest_framework import serializers
from .models import Category, Tag, Post, Comment, LikeAndRating

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name'] 

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'category', 'tags', 'status', 'created_at', 'published_date']
    def validate(self, attrs):
        # If status is plublished, ensure published_date is set
        status = attrs.get('status', getattr(self.instance, 'status', 'draft'))
        published_date = attrs.get('published_date', getattr(self.instance, 'published_date', None))
        if status == 'published' and not published_date:
            raise serializers.ValidationError('Published_date is required when status is published.')
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        if tags:
            post.tags.set(tags)
        return post
    
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance
    
    class CommentSerializer(serializers.ModelSerializer):
        author = serializers.StringRelatedField(read_only=True)
        class Meta:
            model = Comment
            fields = ['id', 'post', 'author', 'content', 'created_at']
            read_only_fields = ['author', 'created_at']
    
class LikeAndRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = LikeAndRating
        fields = ['id', 'post', 'user', 'liked', 'rating', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate_rating(self, value):
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value
    