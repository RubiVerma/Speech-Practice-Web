from django.core.management.base import BaseCommand
from mobi.models import PracticeSentence

class Command(BaseCommand):
    help = 'Load initial practice sentences into the database'

    def handle(self, *args, **kwargs):
        sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "She sells seashells by the seashore.",
            "Practice makes perfect.",
            "Every moment is a fresh beginning.",
            "Silence is sometimes the best answer."
        ]

        for s in sentences:
            PracticeSentence.objects.get_or_create(text=s)

        self.stdout.write(self.style.SUCCESS('Sentences loaded successfully.'))
