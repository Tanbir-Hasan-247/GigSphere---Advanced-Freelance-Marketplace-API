from djoser.serializers import UserCreateSerializer as UCS, UserSerializer as US
from users.models import BuyerProfile, SellerProfile, User

class UserCreateSerializer(UCS):
    class Meta(UCS.Meta):
        fields = ("id", "email", "password", "first_name", "last_name", "role", "phone")

    def create(self, validated_data):
        user = super().create(validated_data)

        role = validated_data.get("role")

        if role == User.SELLER:
            SellerProfile.objects.create(user=user)
        elif role == User.BUYER:
            BuyerProfile.objects.create(user=user)

        return user
    

class UserSerializer(US):
    class Meta(US.Meta):
        fields = ("id", "email", "first_name", "last_name", "role", 'phone')

        ref_name = "custom_user_serializer"  # Add this line to set a unique reference name