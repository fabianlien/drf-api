from rest_framework import generics
from .serializers import ProfileSerializer
from .models import Profile
from drf_api.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListCreateAPIView):
    """
    Lists all profiles
    Instance creation handled by django signals
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Displays a url-specified profile and grants CRUD access
    only if the request user id matches the profile id
    authentication handled by REST custom permissions
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()