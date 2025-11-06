from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Quote, Author, Tag
from .forms import TagForm, QuoteForm, AuthorForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


def main(request, page=1):
    quotes = Quote.objects.order_by("-id")
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.get_page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, "quotes/author_detail_ind.html", context={"author": author})


@login_required
def tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes_app:main")
        else:
            return render(request, "quotes/tag.html", {"form": form})

    return render(request, "quotes/tag.html", {"form": TagForm()})


@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)

            author_name = request.POST.get("author")
            author, created = Author.objects.get_or_create(fullname=author_name)

            new_quote.author = author  # ForeignKey
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            new_quote.tags.set(choice_tags)

            return redirect(to="quotes_app:main")

    return render(
        request,
        "quotes/quote.html",
        {"tags": tags, "authors": authors, "form": QuoteForm()},
    )


@login_required
def author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect(to="quotes_app:main")
    return render(
        request,
        "quotes/author.html",
        {"form": AuthorForm()},
    )
