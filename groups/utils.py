from .models import Group


def create_group_if_not_exists(group):
    found_group = Group.objects.filter(scientific_name__iexact=group["scientific_name"])

    if len(found_group) == 0:
        return Group.objects.create(**group)

    return found_group[0]
