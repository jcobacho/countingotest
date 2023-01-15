from decimal import Decimal

import factory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from taggit.models import TaggedItem, Tag

from inventory.models import Variation, VariationCategory, Product, Category
from core.faker import faker

User = get_user_model()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    name = factory.Iterator(['Drinks', "Hamburgers", "Pizza"])


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = faker.name()
    description = faker.text()
    current_price = factory.lazy_attribute(lambda p: p.price)

    category = factory.SubFactory(CategoryFactory)


class VariationCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VariationCategory

    name = factory.Iterator(['Color', "Size", "Package"])
    description = factory.LazyAttribute(lambda _: faker.text())


class VariationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Variation

    variation_category = factory.SubFactory(VariationCategoryFactory)
    product_group = factory.SubFactory(ProductFactory)


class TaggedItemFactory(factory.django.DjangoModelFactory):
    object_id = factory.SelfAttribute('content_object.id')
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))

    class Meta:
        exclude = ['content_object']
        abstract = True


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Iterator(['red', 'yellow', 'green'])


class OptionVariationFactory(TaggedItemFactory):
    content_object = factory.SubFactory(VariationFactory)
    tag = factory.SubFactory(TagFactory)

    class Meta:
        model = TaggedItem



