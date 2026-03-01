from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.serializers import RegisterSerializer
from core.views import verify_nid_view
from .services import generate_otp, verify_otp

User = get_user_model()


class LoginThrottle(AnonRateThrottle):
    scope = "login"


class IsDevBasicAuthAllowed(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def session_login(request):
    user = authenticate(request, phone=request.data.get("phone"), password=request.data.get("password"))
    if not user:
        return Response({"detail": "Invalid credentials"}, status=401)
    login(request, user)
    return Response({"message": "session login successful"})


@api_view(["POST"])
def universal_logout(request):
    logout(request)
    return Response({"message": "logged out"})


@api_view(["GET"])
def whoami(request):
    auth_method = "jwt" if request.auth else "session"
    return Response({"id": request.user.id, "phone": request.user.phone, "auth_method": auth_method})


class IshemaTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_type"] = user.user_type
        return token


class IshemaTokenObtainView(TokenObtainPairView):
    serializer_class = IshemaTokenSerializer
    throttle_classes = [LoginThrottle]


class IshemaTokenRefreshView(TokenRefreshView):
    pass


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def identity_register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save(is_verified=False)
    otp = generate_otp(user.phone)
    return Response({"id": user.id, "otp": otp, "message": "Account created. Verify OTP."}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def verify_otp_view(request):
    phone = request.data.get("phone", "")
    code = request.data.get("code", "")
    ok = verify_otp(phone, code)
    if not ok:
        return Response({"verified": False}, status=400)
    user = User.objects.get(phone=phone)
    user.is_verified = True
    user.save(update_fields=["is_verified"])
    return Response({"verified": True})


@api_view(["POST"])
def kyc_nid(request):
    return verify_nid_view(request)


@api_view(["GET"])
def identity_status(request):
    return Response({"is_verified": request.user.is_verified, "user_type": request.user.user_type})
