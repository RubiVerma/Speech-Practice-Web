from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import SentenceRecord

@receiver(post_migrate)
def seed_sentences(sender, **kwargs):
    if sender.name != 'mobi':
        return  

    if not SentenceRecord.objects.exists():
        print("🌱 Seeding default practice sentences...")
        user = User.objects.first() 
        if not user:
            user = User.objects.create_user(username='testuser', password='test1234')

        default_sentences = [
            "Welcome to the speech practice app.",
            "Practice makes perfect.",
            "Django is a powerful web framework.",
            "Artificial Intelligence is changing the world.",
            "Speak clearly and confidently.",
        ]

        for text in default_sentences:
            SentenceRecord.objects.create(user=user, sentence=text, spoken_text="", accuracy=0.0)
