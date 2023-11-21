from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Blog, BlogComment
from .serializer import BlogSerializer, BlogCommentSerializer
# Create your views here.

# Define a function-based view for handling GET and POST requests related to blogs
@api_view(['GET', 'POST'])
def blog_list(request):
    # Check if the incoming request is a GET request
    if request.method == 'GET':
        # Retrieve all public blogs from the database using the Blog model
        all_blogs = Blog.objects.filter(is_public=True)
        # Serialize the queryset into JSON data using the BlogSerializer
        serializer = BlogSerializer(all_blogs, many=True)
        
        # Return the serialized data as a response with a 200 OK status
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Check if the incoming request is a POST request
    if request.method == 'POST':
        # Serialize the incoming data from the request using the BlogSerializer
        serializer = BlogSerializer(data=request.data)
        
        # Check if the serialized data is valid
        if serializer.is_valid():
            # Save the valid data to the database
            serializer.save()
            # Return the serialized data as a response with a 201 Created status
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return errors if the serialized data is not valid with a 400 Bad Request status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Define a function-based view for handling GET, PUT, and DELETE requests for a specific blog
@api_view(['GET', 'PUT', 'DELETE'])
def blog_detail(request, pk):
    # Check if the incoming request is a GET request
    if request.method == 'GET':
        # Retrieve a specific public blog from the database using the Blog model and the provided primary key (pk)
        blog = Blog.objects.get(is_public=True, pk=pk)
        # Serialize the retrieved blog into JSON data using the BlogSerializer
        serializer = BlogSerializer(blog)
        # Return the serialized data as a response
        return Response(serializer.data)
    
    # Check if the incoming request is a PUT request
    if request.method == 'PUT':
        # Retrieve the specific blog from the database using the provided primary key (pk)
        blog = Blog.objects.get(pk=pk)
        # Serialize the existing blog with the updated data from the request using the BlogSerializer
        serializer = BlogSerializer(blog, data=request.data)
        
        # Check if the serialized data is valid
        if serializer.is_valid():
            # Save the updated data to the database
            serializer.save()
            # Return the serialized data as a response with a 201 Created status
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return errors if the serialized data is not valid with a 400 Bad Request status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
    # Check if the incoming request is a DELETE request
    if request.method == 'DELETE':
        # Retrieve the specific blog from the database using the provided primary key (pk)
        blog = Blog.objects.get(pk=pk)
        # Delete the specified blog from the database
        blog.delete()
        # Return an empty response
        return Response()
    
@api_view(['GET', 'POST'])
def blog_comment(request, pk):
    if request.method == 'GET':
        # Handle GET request logic if needed
        # For example, retrieve and return existing comments for the specified blog
        comments = BlogComment.objects.filter(blog=pk)
        serializer = BlogCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # blog = Blog.objects.get(pk=pk)
        blog=get_object_or_404(Blog, pk=pk)
        comment_data = {'description': request.data.get('description'), 'blog': blog.pk}
        serializer = BlogCommentSerializer(data=comment_data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Comment saved'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)