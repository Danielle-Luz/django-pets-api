from rest_framework import serializers
from .models import SexPet
from groups.serializers import GroupSerializer
from traits.serializers import TraitsSerializer
from rest_framework.validators import UniqueValidator
from django.utils.functional import lazy
from .models import Pet


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        max_length=50, validators=[UniqueValidator(queryset=Pet.objects.all())]
    )
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=SexPet.choices, required=False)

    group = GroupSerializer()
    traits = TraitsSerializer(many=True)


class PetUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        max_length=50,
        validators=[UniqueValidator(queryset=Pet.objects.all())],
        required=False,
    )
    age = serializers.IntegerField(required=False)
    weight = serializers.FloatField(required=False)
    sex = serializers.ChoiceField(choices=SexPet.choices, required=False)

    group = GroupSerializer(required=False)
    traits = TraitsSerializer(many=True, required=False)
