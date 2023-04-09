from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .serializers import PetSerializer, PetUpdateSerializer
from traits.models import Trait
from .models import Pet
from groups.utils import create_group_if_not_exists
from traits.utils import create_trait_if_not_exists


class PetView(APIView, PageNumberPagination):
    def get(self, request):
        searched_trait = request.query_params.get("trait", None)
        if searched_trait != None:
            found_pets = Pet.objects.filter(traits__name__iexact=searched_trait)
        else:
            found_pets = Pet.objects.all()

        pets_paginated = self.paginate_queryset(found_pets, request, view=self)
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


class PetInfoView(APIView):
    def get(self, request, pet_id):
        try:
            found_pet = PetSerializer(Pet.objects.get(id=pet_id)).data

            return Response(found_pet)
        except:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

    def patch(self, request, pet_id):
        try:
            found_pet = Pet.objects.get(id=pet_id)
            new_pet_info = PetUpdateSerializer(data=request.data)

            if new_pet_info.is_valid():
                if "traits" in new_pet_info.validated_data.keys():
                    pet_traits = new_pet_info.validated_data.pop("traits")
                    created_or_found_traits = create_trait_if_not_exists(
                        pet_traits, found_pet
                    )

                    found_pet.traits.set(created_or_found_traits)

                if "group" in new_pet_info.validated_data.keys():
                    pet_group = create_group_if_not_exists(
                        new_pet_info.validated_data.pop("group")
                    )
                    Pet.objects.update(
                        id=pet_id, **new_pet_info.validated_data, group=pet_group
                    )
                else:
                    Pet.objects.update(id=pet_id, **new_pet_info.validated_data)

                updated_pet = Pet.objects.get(id=pet_id)
                return Response(
                    PetUpdateSerializer(updated_pet).data, status.HTTP_200_OK
                )

            return Response(new_pet_info.errors, status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

    def delete(self, request, pet_id):
        try:
            found_pet = Pet.objects.get(id=pet_id)

            found_pet.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)
