from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
def home(request):
    questions = Question.objects.all().order_by('-created_at')
    question_form = QuestionForm()
    answer_forms = {q.id: AnswerForm() for q in questions}
    login_form = AuthenticationForm()
    
    return render(request, 'home.html', {
        'questions': questions,
        'question_form': question_form,
        'answer_forms': answer_forms,
        'form': login_form  # <-- Add this line
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to the home page or any other page
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            # Login failed - render home with the form containing errors
            questions = Question.objects.all().order_by('-created_at')
            question_form = QuestionForm()
            answer_forms = {q.id: AnswerForm() for q in questions}
            return render(request, 'home.html', {
                'questions': questions,
                'question_form': question_form,
                'answer_forms': answer_forms,
                'form': form
            })
    return redirect('home')


@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_by = request.user
            question.save()
            return redirect('home')
    return redirect('home')

@login_required
def submit_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.answered_by = request.user
            answer.save()
            return redirect('home')
    return redirect('home')

@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user in answer.likes.all():
        answer.likes.remove(request.user)
        liked = False
    else:
        answer.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'like_count': answer.likes.count()})