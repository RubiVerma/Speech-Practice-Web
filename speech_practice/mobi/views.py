from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import SentenceRecord, PracticeSentence
from django.views.decorators.csrf import csrf_exempt
import json
from difflib import SequenceMatcher
from django.db.models import Avg
from django.contrib.auth.forms import UserCreationForm



def home(request):
    return render(request, 'home.html')

@login_required
def practice(request):
    index = request.session.get('index', 0)
    sentences = PracticeSentence.objects.all()

    if not sentences.exists():
        return render(request, 'practice.html', {'sentence': 'No records found'})

    if index >= len(sentences):
        index = 0
        request.session['index'] = 0

    sentence = sentences[index].text
    return render(request, 'practice.html', {'sentence': sentence})

@csrf_exempt
@login_required
def check(request):
    data = json.loads(request.body)
    reference = data.get("reference", "").lower().strip()
    spoken = data.get("spoken", "").lower().strip()

    ratio = SequenceMatcher(None, reference, spoken).ratio()
    accuracy = round(ratio * 100, 2)

    SentenceRecord.objects.create(
        user=request.user,
        sentence=reference,
        spoken_text=spoken,
        accuracy=accuracy
    )

    request.session['index'] = request.session.get('index', 0) + 1
    sentences = PracticeSentence.objects.all()
    next_index = request.session['index']
    if next_index >= len(sentences):
        next_index = 0
        request.session['index'] = 0

    new_sentence = sentences[next_index].text if sentences else "No more sentences."

    return JsonResponse({"accuracy": accuracy, "new_sentence": new_sentence})

@login_required
def next_sentence(request):
    total = PracticeSentence.objects.count()
    request.session['index'] = min(request.session.get('index', 0) + 1, total - 1)
    sentence = PracticeSentence.objects.all()[request.session['index']].text
    return JsonResponse({
        "sentence": sentence,
        "has_previous": request.session['index'] > 0,
        "has_next": request.session['index'] < total - 1
    })

@login_required
def previous_sentence(request):
    request.session['index'] = max(request.session.get('index', 0) - 1, 0)
    sentence = PracticeSentence.objects.all()[request.session['index']].text
    total = PracticeSentence.objects.count()
    return JsonResponse({
        "sentence": sentence,
        "has_previous": request.session['index'] > 0,
        "has_next": request.session['index'] < total - 1
    })

@login_required
def progress(request):
    records = SentenceRecord.objects.filter(user=request.user)
    total = records.count()
    avg_accuracy = round(records.aggregate(Avg('accuracy'))['accuracy__avg'] or 0, 2)
    return render(request, "progress.html", {
        "total": total,
        "average": avg_accuracy,
        "records": records
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    return render(request, 'login.html')
def logged_out(request):
    return render(request, 'logged_out.html')