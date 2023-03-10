from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer

# Create your views here.


class UserListView(APIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({"message": "Please Login"})
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
