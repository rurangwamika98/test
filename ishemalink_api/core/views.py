from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import NIDVerifySerializer, RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def verify_nid_view(request):
    serializer = NIDVerifySerializer(data=request.data)
    if serializer.is_valid():
        return Response({"valid": True})
    return Response({"valid": False, "error": serializer.errors.get("nid", ["Invalid NID"])[0]}, status=400)


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class AgentOnboardView(generics.UpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.user_type = "AGENT"
        user.nid_number = request.data.get("nid_number", "")
        user.assigned_sector = request.data.get("assigned_sector", "")
        user.full_clean()
        user.save()
        return Response(UserSerializer(user).data)
