from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from urllib3 import request
from consultation_packages.models import ConsultationPackage
from subscriptions.models import Subscription
from .models import Payment
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from .forms import CheckoutForm
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now


@login_required
def checkout(request, package_id):
    package = get_object_or_404(ConsultationPackage, id=package_id)

    subscription = Subscription.objects.filter(user=request.user).first()
    discount = subscription.discount_percentage() if subscription else 0

    # Decide original amount
    original_amount = (
        package.min_price if package.min_price else package.max_price
    )

    # Apply discount
    final_amount = original_amount - (original_amount * discount / 100)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():

            payment = Payment.objects.create(
                user=request.user,
                package=package,

                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                original_amount=original_amount,
                discount_percent=discount,
                final_amount=final_amount,
            )
            stripe.api_key = settings.STRIPE_API_KEY

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                customer_email=payment.email,
                line_items=[{
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': package.title,
                        },
                        'unit_amount': int(final_amount * 100),
                    },
                    'quantity': 1,
                }],

                success_url=request.build_absolute_uri(
                    reverse('payments:success', args=[payment.id])
                ),

                cancel_url=request.build_absolute_uri(
                    reverse('payments:checkout', args=[package.id])
                ),
            )

            payment.stripe_session_id = session.id
            payment.save()

            return redirect(session.url)

    else:
        form = CheckoutForm(
            initial={
                'email': request.user.email
            }
        )

    # ✅ THIS MUST ALWAYS RUN
    context = {
        'package': package,
        'original_amount': original_amount,
        'discount': discount,
        'final_amount': final_amount,
        'subscription': subscription,
        'form': form,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    }

    return render(request, 'payments/checkout.html', context)


@login_required
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    stripe.api_key = settings.STRIPE_API_KEY
    session = stripe.checkout.Session.retrieve(payment.stripe_session_id)

    if session.payment_status == 'paid':
        payment.mark_completed()


        # updat subscription

        if payment.payment_type == Payment.SUBSCRIPTION:
            subscription, _ = Subscription.objects.get_or_create(
                user=request.user
            )

            subscription.plan = payment.subscription_plan
            subscription.started_at = timezone.now()

            if payment.subscription_plan == 'basic':
                subscription.expires_at = timezone.now() + timedelta(days=90)
            elif payment.subscription_plan == 'full':
                subscription.expires_at = timezone.now() + timedelta(days=90)

            subscription.save()

    return render(request, 'payments/payment_success.html', {'payment': payment})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment = Payment.objects.filter(stripe_session_id=session.id).first()
        if payment:
            payment.mark_completed()

    return HttpResponse(status=200)


@login_required
def payment_history(request):
    payments = Payment.objects.filter(
        user=request.user).order_by('-created_at')
    return render(request, 'payments/payment_history.html', {'payments': payments})


@login_required
def payment_delete(request, payment_id):
    # Try to get the payment for this user
    payment = Payment.objects.filter(id=payment_id, user=request.user).first()

    if not payment:
        messages.error(request, "Payment not found or you cannot delete it.")
        return redirect('payments:history')  # redirect to payment history

    if request.method == 'POST':
        payment.delete()
        messages.success(request, "Payment deleted successfully.")
        return redirect('payments:history')

    # Optional: render confirmation page
    return redirect('payments:history')


@login_required
def subscription_checkout(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    if request.method == 'POST':

        stripe.api_key = settings.STRIPE_API_KEY

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',

            line_items=[{
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': f"{payment.subscription_plan.capitalize()} Subscription",
                    },
                    'unit_amount': int(payment.final_amount * 100),
                },
                'quantity': 1,
            }],
            success_url=request.build_absolute_uri(
                reverse('payments:success', args=[payment.id])
            ),
            cancel_url=request.build_absolute_uri(
                reverse('subscriptions:list')
            ),
        )

        payment.stripe_session_id = session.id
        payment.save()

        return redirect(session.url)

    else:
        context = {
            'payment_id': payment_id,
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
            'payment': payment,
            'final_amount': payment.final_amount,
        }

        return render(request, 'payments/subscription_checkout.html', context)


@login_required
def subscription_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    stripe.api_key = settings.STRIPE_API_KEY
    session = stripe.checkout.Session.retrieve(payment.stripe_session_id)

    if session.payment_status == 'paid':
        payment.mark_completed()

        subscription, _ = Subscription.objects.get_or_create(
            user=request.user
        )

        subscription.activate(payment.subscription_plan)
        subscription.refresh_from_db()

    return redirect('subscriptions:my_subscription')
