from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'A description of what this command does'

    def handle(self, *args, **options):
        self.stdout.write("My sample command output")




