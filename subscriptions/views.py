from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Subscription
from payments.models import Payment
from django.utils import timezone
from django.utils.timezone import now



@login_required
def subscription_list(request):
    subscription, created = Subscription.objects.get_or_create(user=request.user, defaults={'plan': 'none'})
    return render(request, 'subscriptions/subscription_list.html', {
        'current_plan': subscription.plan
    })




@login_required
def buy_subscription(request, plan):
    subscription, _ = Subscription.objects.get_or_create(user=request.user, defaults={'plan': 'none'})

    if plan in ['none', 'basic', 'full']:
        subscription.plan = plan
        subscription.save()

    return redirect('subscriptions:list')


@login_required
def subscription_checkout(request, plan):

    if plan not in ['basic', 'full']:
        return redirect('subscriptions:list')
    
    subscription, _ = Subscription.objects.get_or_create(user=request.user)


    amount = Subscription.PRICE_MAP[plan]
    payment = Payment.objects.create(
        user=request.user,
        package=None,
        original_amount=amount,
        discount_percent=0,
        final_amount=amount
    )

    request.session['subscription_plan'] = plan

    #  redirect to PAYMENTS app
    return redirect(
        'payments:subscription_checkout',
        payment_id=payment.id
    )
    


@login_required
def renew_subscription(request, plan):
    subscription = get_object_or_404(Subscription, user=request.user)
    return redirect('subscriptions:checkout', plan=plan)


@login_required
def my_subscription(request):
    subscription = Subscription.objects.filter(user=request.user).first()

    bought_packages = Payment.objects.filter(
        user=request.user,
        status=Payment.COMPLETED
        ).select_related( 'package__lawyer')
      # , package__isnull=False
    #).select_related(
     #   'package',
      #  'package__lawyer').order_by('-created_at')
    
    
    context = {
        'user': request.user,
        'subscription': subscription,
        'bought_packages': bought_packages,
        'today': timezone.now()
    }

    return render(request, 'subscriptions/my_subscription.html', context)


