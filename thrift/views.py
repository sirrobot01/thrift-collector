from rest_framework import generics


class UserRegistration(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserRegistrationSerializer
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.to_representation(instance=serializer.instance),
                        status=status.HTTP_201_CREATED)