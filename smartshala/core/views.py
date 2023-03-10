from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer

# Create your views here.


class UserListView(ListCreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({"message": "Please Login"})
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
