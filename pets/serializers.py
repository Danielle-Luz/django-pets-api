from rest_framework import serializers
from .models import SexPet
from groups.serializers import GroupSerializer
from traits.serializers import TraitsSerializer
from rest_framework.validators import UniqueValidator
from groups.utils import create_group_if_not_exists
from traits.utils import create_trait_if_not_exists
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
