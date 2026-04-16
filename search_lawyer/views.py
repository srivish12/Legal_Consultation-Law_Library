from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from .models import Lawyer
from consultation_packages.models import ConsultationPackage
from .forms import LawyerForm

def search_lawyer(request):
    """
    Search and filter lawyers
    """
    q = request.GET.get('q', '')
    lawyer_type = request.GET.get('type', '')
    specialty = request.GET.get('specialty', '')
    court_level = request.GET.get('court_level', '')

    lawyers = Lawyer.objects.filter(is_available=True)

    # Search by name or bio
    if q:
        lawyers = lawyers.filter(
            Q(name__icontains=q) |
            Q(bio__icontains=q) |
            Q(specialty__icontains=q) |
            Q(court_level__icontains=q)
        )

    # Filter by lawyer type
    if lawyer_type:
        lawyers = lawyers.filter(lawyer_type=lawyer_type)

    # Solicitor specialty filter
    if specialty:
        lawyers = lawyers.filter(specialty=specialty)

    # Advocate court level filter
    if court_level:
        lawyers = lawyers.filter(court_level=court_level)

    context = {
        'lawyers': lawyers,
        'q': q,
        'lawyer_type': lawyer_type,
        'specialty': specialty,
        'court_level': court_level,
    }

    return render(request, 'search_lawyer/search_results.html', context)


def search_form(request):
    """
    Display search form
    """

    return render(request, 'search_lawyer/search_form.html')


def lawyer_details(request, slug):
    """
    Lawyer profile / detail page
    """
    lawyer = get_object_or_404(Lawyer, slug=slug)
    # Fetch consultation packages for the lawyer
    packages = ConsultationPackage.objects.filter(lawyer=lawyer)

    return render(request, 'search_lawyer/lawyer_detail.html', {
        'lawyer': lawyer,
        'packages': packages
    })

@login_required
@permission_required('search_lawyer.add_lawyer', raise_exception=True)
def create_lawyer(request):
    if request.method == 'POST':
        form = LawyerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('search_lawyer')
    else:
        form = LawyerForm()

    return render(request, 'search_lawyer/create_lawyer.html', {'form': form})


@login_required
@permission_required('search_lawyer.change_lawyer', raise_exception=True)
def edit_lawyer(request, lawyer_id):
    lawyer = get_object_or_404(Lawyer, id=lawyer_id)

    if request.method == 'POST':
        form = LawyerForm(request.POST, instance=lawyer)
        if form.is_valid():
            form.save()
            return redirect('lawyer_details', slug=lawyer.slug)
    else:
        form = LawyerForm(instance=lawyer)

    return render(request, 'search_lawyer/lawyer_form.html', {'form': form})


@login_required
@permission_required('search_lawyer.delete_lawyer', raise_exception=True)
def delete_lawyer(request, lawyer_id):
    lawyer = get_object_or_404(Lawyer, id=lawyer_id)

    if request.method == 'POST':
        lawyer.delete()
        return redirect('search_lawyer')

    return render(request, 'search_lawyer/lawyer_confirm_delete.html', {'lawyer': lawyer})