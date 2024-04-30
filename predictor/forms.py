from django import forms


class QueryForm(forms.Form):
    query_text = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 5, "cols": 40, "maxlength": 2000, "class": "query-textarea"}
        ),
        label="",
    )
