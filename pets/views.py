from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .serializers import PetSerializer
from .models import Pet
from groups.utils import create_group_if_not_exists
from traits.utils import create_trait_if_not_exists


class PetView(APIView, PageNumberPagination):
    def get(self, request):
        all_pets = Pet.objects.all()

        pets_paginated = self.paginate_queryset(all_pets, request, view=self)
        serialized_pets = PetSerializer(pets_paginated, many=True).data

        return self.get_paginated_response(serialized_pets)

    def post(self, request):
        new_pet = PetSerializer(data=request.data)

        if new_pet.is_valid():
            pet_group = create_group_if_not_exists(new_pet.validated_data.pop("group"))
            pet_traits = new_pet.validated_data.pop("traits")

            created_pet = Pet.objects.create(**new_pet.validated_data, group=pet_group)

            create_trait_if_not_exists(pet_traits, created_pet)

            return Response(PetSerializer(created_pet).data, status.HTTP_201_CREATED)

        return Response(new_pet.errors, status.HTTP_400_BAD_REQUEST)
