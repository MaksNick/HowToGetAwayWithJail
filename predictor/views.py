from django.shortcuts import render, get_object_or_404, redirect
from .forms import QueryForm
from .models import QueryHistory
from django.http import JsonResponse

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

import pickle
import sklearn


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

            with open("./model.pickle", "rb") as f:
                model = pickle.load(f)
            pos_proba = model.predict_proba([query_text])[0][1]

            if pos_proba < 0.5:
                predicted_outcome = (f"Точно не стоит. По моим данным, вероятность попасть в тюрьму за такое "
                                     f"составляет {(1 - pos_proba):.3f}.")
            elif pos_proba < 0.8:
                predicted_outcome = (f"Сомнительно. У судов бывали разные решения по этому поводу. С вероятностью "
                                     f"{pos_proba:.3f} всё обойдётся!")
            else:
                predicted_outcome = f"Всё будет хорошо (с вероятностью {pos_proba:.3f}) :)"

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
