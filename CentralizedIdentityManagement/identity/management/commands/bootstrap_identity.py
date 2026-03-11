from django.core.management.base import BaseCommand
from identity.bootstrap import bootstrap_system


class Command(BaseCommand):
    help = "Bootstrap initial identity configuration"

    def handle(self, *args, **options):
        bootstrap_system()
        self.stdout.write(
            self.style.SUCCESS("Initial identity configuration completed.")
        )
