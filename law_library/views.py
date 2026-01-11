from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import LawBook


def book_list(request):
    query = request.GET.get('q', '').strip()
    subject = request.GET.get('subject', '').strip()
    alphabet = request.GET.get('alphabet', '').strip()

    books = LawBook.objects.all()

    # Search by title or author
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    # Filter by subject (exact match recommended)
    if subject:
        books = books.filter(subject=subject)

    # Filter by starting alphabet of title (BEST PRACTICE)
    if alphabet:
        books = books.filter(title__istartswith=alphabet)

    # Dropdown data (clean + ordered)
    alphabets = (
        LawBook.objects
        .exclude(title__isnull=True)
        .exclude(title__exact='')
        .values_list('title', flat=True)
    )

    alphabets = sorted({title[0].upper() for title in alphabets})

    subjects = (
        LawBook.objects
        .exclude(subject__isnull=True)
        .exclude(subject__exact='')
        .values_list('subject', flat=True)
        .distinct()
        .order_by('subject')
    )

    context = {
        'books': books,
        'alphabets': alphabets,
        'subjects': subjects,
        'query': query,
        'subject': subject,
        'alphabet': alphabet,
    }

    return render(request, 'book_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(LawBook, pk=pk)
    return render(request, 'book_detail.html', {'book': book})

