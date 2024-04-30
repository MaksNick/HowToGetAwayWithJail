from django.shortcuts import render, get_object_or_404, redirect
from .forms import QueryForm
from .models import QueryHistory
from django.http import JsonResponse

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("predict_legal_outcome")
            else:
                # Handle invalid credentials (e.g., display an error message)
                print("Invalid username or password")
        else:
            print(form.errors)  # Inspect form errors for debugging
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("predict_legal_outcome")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("predict_legal_outcome")


def predict_legal_outcome(request):
    predicted_outcome = None

    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            query_text = form.cleaned_data["query_text"]
            """
            Бери текст из query_text, прогоняй и засунь в predicted_outcome вместо плейсходера
            """
            predicted_outcome = "This is a placeholder for the predicted outcome."

            if request.user.is_authenticated:
                query_history = QueryHistory.objects.create(
                    query_text=query_text,
                    user=request.user,
                    predicted_outcome=predicted_outcome,
                )
                return redirect("query_detail", query_id=query_history.id)
    else:
        form = QueryForm()

    query_history = []
    if request.user.is_authenticated:
        query_history = QueryHistory.objects.filter(user=request.user).order_by(
            "-timestamp"
        )

    return render(
        request,
        "main.html",
        {
            "form": form,
            "query_history": query_history,
            "predicted_outcome": predicted_outcome,
        },
    )


def query_detail(request, query_id):
    query_detail = get_object_or_404(QueryHistory, pk=query_id)
    return render(request, "question.html", {"query_detail": query_detail})
