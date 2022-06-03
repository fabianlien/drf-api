from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProfileSerializer
from .models import Profile
from drf_api.permissions import IsOwnerOrReadOnly


class ProfileList(APIView):
    """
    Lists all profiles
    Instance creation handled by django signals
    """
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data)


class ProfileDetail(APIView):
    """
    Displays a url-specified profile and grants CRUD access
    only if the request user id matches the profile id
    authentication handled by REST custom permissions
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist():
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk=pk)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk=pk)
        self.check_object_permissions(self.request, profile)
        serializer = ProfileSerializer(
            profile,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
