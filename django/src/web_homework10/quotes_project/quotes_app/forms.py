from django.forms import ModelForm, CharField, TextInput, Textarea
from .models import Tag, Quote, Author


class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ["name"]


class QuoteForm(ModelForm):

    quote = CharField(
        widget=Textarea(
            attrs={
                "class": "form-control",
                "id": "exampleFormControlTextarea1",
                "rows": 3,
                "placeholder": "Type your quote here...",
            }
        )
    )

    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ["tags", 'author']


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
        widgets = {
            "fullname": TextInput(
                attrs={"class": "form-control", "placeholder": "Albert Einstein"}
            ),
            "born_date": TextInput(
                attrs={"class": "form-control", "placeholder": "March 14, 1879"}
            ),
            "born_location": TextInput(
                attrs={"class": "form-control", "placeholder": "in Ulm, Germany"}
            ),
            "description": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Коротка біографія автора...",
                }
            ),
        }
