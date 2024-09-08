from typing import Dict

from catalog.models import Bouquet, City, Package


def create_bouquet(b_data: Dict) -> Bouquet:
    new_bouquet = Bouquet.objects.create(
        bouquet_type = Bouquet.IB,
        city=City.objects.get(pk=1),
        package=Package.objects.get(name=b_data.get('package')),
        price=b_data.get('price'),
        is_reserved=True,
    )

    return new_bouquet

