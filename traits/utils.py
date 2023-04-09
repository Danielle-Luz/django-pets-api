from .models import Trait


def create_trait_if_not_exists(traits, pet):
    created_or_found_traits = []

    for trait in traits:
        found_trait = Trait.objects.filter(name__iexact=trait["name"])

        if len(found_trait) == 0:
            found_trait = Trait.objects.create(**trait)
        else:
            found_trait = found_trait[0]

        found_trait.pets.add(pet)

        created_or_found_traits.append(found_trait)
    
    return created_or_found_traits