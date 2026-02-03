from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Subscription
from payments.models import Payment
from django.utils import timezone
from django.utils.timezone import now


@login_required
def subscription_list(request):
    subscription, _ = Subscription.objects.get_or_create(
        user=request.user, defaults={'plan': 'none'})
    return render(request, 'subscriptions/subscription_list.html', {
        'current_plan': subscription.plan
    })


@login_required
def subscription_checkout(request, plan):

    if plan not in ['basic', 'full']:
        return redirect('subscriptions:list')

    subscription, _ = Subscription.objects.get_or_create(user=request.user)

    amount = Subscription.PRICE_MAP[plan]
    payment = Payment.objects.create(
        user=request.user,
        payment_type=Payment.SUBSCRIPTION,  # important
        subscription_plan=plan,
        package=None,
        original_amount=amount,
        discount_percent=0,
        final_amount=amount
    )

    #  redirect to PAYMENTS app
    return redirect(
        'payments:subscription_checkout',
        payment_id=payment.id
    )


@login_required
def renew_subscription(request, plan):

    return redirect('subscriptions:checkout', plan=plan)


@login_required
def my_subscription(request):
    try:
        subscription = request.user.subscription
    except Subscription.DoesNotExist:
        subscription = None

    bought_packages = Payment.objects.filter(
        user=request.user,

        status=Payment.COMPLETED
        ).select_related('package__lawyer',)

    context = {
        'user': request.user,
        'subscription': subscription,
        'bought_packages': bought_packages,
        'today': timezone.now()
    }

    return render(request, 'subscriptions/my_subscription.html', context)
