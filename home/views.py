from django.shortcuts import render
from review.models import PackageReview, LawyerReview


# Create your views here.
def home_page(request):

    latest_package_reviews = PackageReview.objects.select_related(
        'package', 'user'
    ).order_by('-created_at')[:5]

    latest_lawyer_reviews = LawyerReview.objects.select_related(
        'lawyer', 'user'
    ).order_by('-created_at')[:5]
    context = {
        'latest_package_reviews': latest_package_reviews,
        'latest_lawyer_reviews': latest_lawyer_reviews,
    }

    return render(request, 'home/main_page.html', context)
