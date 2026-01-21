from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import  PackageReview
from .forms import  PackageReviewForm
from consultation_packages.models import ConsultationPackage

from payments.models import Payment
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@login_required
def add_package_review(request, package_id):
    package = get_object_or_404(ConsultationPackage, id=package_id)


    if not Payment.objects.filter(user=request.user, package=package,
                                   status=Payment.COMPLETED, paid_at__isnull=False).exists():
        return redirect('package_detail', package_id)


    review = PackageReview.objects.filter(user=request.user, package=package).first()


    if request.method == 'POST':
        form = PackageReviewForm(request.POST, instance=review)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.package = package
            new_review.save() 
            return redirect('package_detail', package_id)
    else:
        form = PackageReviewForm(instance=review)


    return render(request, 'reviews/package_review_form.html', {
        'form': form,
        'package': package
    })





def load_more_package_reviews(request):
    page = request.GET.get('page', 1)

    reviews_qs = (
        PackageReview.objects
        .select_related('package', 'package__lawyer', 'user')
        .order_by('-created_at')
    )

    paginator = Paginator(reviews_qs, 3) # 3 reviews per page 

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        return JsonResponse({
            'reviews': [],
            'has_next': False
        })

    data = [
        {
            'package': review.package.title,
            'lawyer': review.package.lawyer.name,
            'rating': review.rating,
            'comment': review.comment,
            'user': review.user.username,
        }
        for review in page_obj
    ]

    return JsonResponse({
        'reviews': data,
        'has_next': page_obj.has_next()
    })
