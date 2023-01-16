import factory
from django.contrib.auth import get_user_model

from announcement.models import Announcement, Technology
from core.faker import faker

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    first_name = faker.unique.last_name()
    last_name = faker.unique.last_name()
    username = faker.user_name()


class AnnouncementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Announcement
    name = factory.Iterator(['Oddo Course', "Fullstack 2022 full course", "Free Design Course"])


class TechnologyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Technology
    name = faker.unique.name()

