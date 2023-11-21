from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializer import UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated



# View to register a new user
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        # Create an instance of the UserRegistrationSerializer with the request data
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Save the user to the database
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        # Return validation errors if the serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
# View to handle user login
@api_view(['POST'])
def user_login(request):
    # Retrieve username and password from the request data
    user_name = request.data.get('username')
    pass_word = request.data.get('password')
    
    if user_name is None or pass_word is None:
        # Return an error response if either username or password is missing
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Authenticate the user using Django's authenticate function
    user = authenticate(username=user_name, password=pass_word)
    if user is not None:
        # User is authenticated, generate and return the token
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        # User authentication failed, return an error response
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# View to update user information
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    # Retrieve the authenticated user making the request
    user = request.user
    # Create an instance of the UserRegistrationSerializer with the authenticated user and request data
    serializer = UserRegistrationSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        # Save the updated user information
        serializer.save()
        return Response({'message': 'User information updated successfully'}, status=status.HTTP_200_OK)
    # Return validation errors if the serializer is not valid
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View to delete the authenticated user
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    # Retrieve the authenticated user making the request
    user = request.user
    # Delete the authenticated user
    user.delete()
    return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)