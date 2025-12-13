from django.shortcuts import render
from .models import Lawyer
from django.db.models import Q


def search_lawyer(request):
    q = request.GET.get('q', '')
    lawyer_type = request.GET.get('type') # 'solicitor' or 'advocate'
    queryset = Lawyer.objects.all()
    if q:
        queryset = queryset.filter(Q(name__icontains=q) | Q(bio__icontains=q))
    if lawyer_type:
        queryset = queryset.filter(lawyer_type=lawyer_type)

    # additional filters can be applied by specialty or court_level
    if lawyer_type == Lawyer.SOLICITOR:
        speciality = request.GET.get('speciality')
        if speciality:
            queryset = queryset.filter(speciality=speciality)
    elif lawyer_type == Lawyer.ADVOCATE:
        court_level = request.GET.get('court_level')
        if court_level:
            queryset = queryset.filter(court_level=court_level)
    return render(request, 'search_lawyer/search_form.html', {'lawyer': queryset})