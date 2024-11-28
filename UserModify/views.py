from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from config import settings
from django.conf import settings
from .models import UserVoid
from .serializers import UserVoidSignupSerializer
from .serializers import UserVoidLoginSerializer
from rest_framework.views import APIView
from .serializers import UserVoidLogoutSerializer
from .serializers import PasswordChangeSerializer
from .serializers import UserVoidEditSerializer
from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail




User = get_user_model()

# The Black Sun's views

#region register

class UserVoidSignupView(CreateAPIView):

    queryset = UserVoid.objects.all()
    serializer_class = UserVoidSignupSerializer
    permission_classes = [AllowAny]  # Anyone can sign up, no authentication required

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)  # Get the request data
        serializer.is_valid(raise_exception=True)  # Validate the data

        self.perform_create(serializer)  # Create the user (calls serializer's create method)
        headers = self.get_success_headers(serializer.data)  # Generate response headers

        return Response(
            {"message": "User created successfully", "user": serializer.data}, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

#endregion

#region Account stuff

class UserVoidLoginView(APIView):


    def post(self, request, *args, **kwargs):
        # Create a serializer instance with the incoming request data
        serializer = UserVoidLoginSerializer(data=request.data)

        # Validate the request data
        if serializer.is_valid():
            tokens = serializer.save()  # Get the tokens from the serializer
            
            access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

            # Set cookies for access and refresh tokens
            response = Response({
                "message": "Login successful",
                "user": tokens['user'],  # Return user info
                "access": tokens['access'],  # Include access token
                "refresh": tokens['refresh'],  # Include refresh token
            }, status=status.HTTP_200_OK)

            # Set access and refresh tokens in HTTP-only cookies
            response.set_cookie(
                key="access_token",
                value=tokens["access"],
                httponly=True,
                secure=True,
                max_age=int(access_token_lifetime.total_seconds()),
            )
            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh"],
                httponly=True,
                secure=True,
                max_age=int(refresh_token_lifetime.total_seconds()),
            )
            return response
        
        # If invalid, return error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py




class UserVoidLogoutView(APIView):
    def post(self, request):
        # Pass the refresh token to the LogoutSerializer
        serializer = UserVoidLogoutSerializer(data=request.data)
        
        # If the token is valid and successfully blacklisted, clear the cookies
        if serializer.is_valid():
            serializer.save()
            
            # Prepare response
            response = Response({"detail": "Logout successful"}, status=status.HTTP_204_NO_CONTENT)
            
            # Clear cookies
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            
            return response
        
        # If there are validation errors, return them
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class UserVoidSoftDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.soft_delete()  # Call the model's soft delete method
        return Response(
            {"message": "Account soft deleted successfully. You can reactivate it within 30 days."},
            status=status.HTTP_204_NO_CONTENT
        )



class UserVoidHardDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.hard_delete()  # Call the model's hard delete method
        return Response(
            {"message": "Account permanently deleted."},
            status=status.HTTP_204_NO_CONTENT
        )










class UserVoidReactivateView(APIView):
    permission_classes = [permissions.IsAuthenticated] 

    def post(self, request, *args, **kwargs):
     
        username = request.data.get('username')
        

        user = User.objects.filter(username=username, is_active=False).first()
        
      
        if not user or not user.deleted_at or (timezone.now() - user.deleted_at > timedelta(days=30)):
            return Response({"message": "Account reactivation unavailable."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Reactivate the user
        user.is_active = True
        user.deleted_at = None  # Remove the deletion timestamp
        user.save()
        
        return Response({"message": "Account reactivated successfully."}, status=status.HTTP_200_OK)



#region Profile


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)










class UserVoidEditView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can edit their info

    def get(self, request):
        """Return the user's current information."""
        user = request.user
        serializer = UserVoidEditSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        """Update user information and trigger email verification if email is changed."""
        user = request.user
        serializer = UserVoidEditSerializer(user, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            updated_user = serializer.save()  # Save updates to user instance
            
            # Send verification email if email was changed
            if updated_user.email != user.email:
                self.send_verification_email(updated_user)

            return Response(
                {"message": "User information updated successfully", "user": serializer.data}, 
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_email(self, user):
        """Send the email verification link to the user."""
        verification_link = f"{settings.FRONTEND_URL}/verify-email/?token={user.verification_token}"

        send_mail(
            'Verify your email address',
            f"Please verify your new email address by clicking the following link: {verification_link}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )







class VerifyEmailView(APIView):
    def get(self, request, *args, **kwargs):
        """Verify the user's email using the verification token."""
        token = request.GET.get("token")
        
        if not token:
            return Response({"message": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Find the user by verification token
        user = User.objects.filter(verification_token=token).first()

        if user:
            # Confirm the email and clear the token
            user.email_verified = True
            user.verification_token = None  # Clear the token after successful verification
            user.save()
            return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)

        return Response({"message": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

#endregion
