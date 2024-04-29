from django.shortcuts import render, get_object_or_404, redirect
from .forms import QueryForm
from .models import QueryHistory


from django.shortcuts import render, redirect
from .forms import QueryForm
from .models import QueryHistory


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
