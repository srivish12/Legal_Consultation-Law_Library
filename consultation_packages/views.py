from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import ConsultationPackage
from search_lawyer.models import Lawyer
from .forms import ConsultationPackageForm



@staff_member_required
def create_package(request):
    if request.method == 'POST':
        form = ConsultationPackageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('packages_list')
    else:
        form = ConsultationPackageForm()

    return render(request, 'consultation_packages/create_package.html', {
        'form': form
    })



def package_list(request):
    packages = ConsultationPackage.objects.all()
    return render(request, 'consultation_packages/package_list.html', {'packages': packages})




def package_detail(request, pk, ):
    package = get_object_or_404(ConsultationPackage, pk=pk)
    lawyer = package.lawyer

    return render(request, 'consultation_packages/package_detail.html', {'package': package, 'lawyer': lawyer})
