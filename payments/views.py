from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from consultation_packages.models import ConsultationPackage
from subscriptions.models import Subscription
from .models import Payment
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone


@login_required
def checkout(request, package_id):
	package = get_object_or_404(ConsultationPackage, id=package_id)

	subscription, _ = Subscription.objects.get_or_create(user=request.user)
	discount = subscription.discount_percentage()

	# Decide original amount
	if package.min_price:
		original_amount = package.min_price
	else:
		original_amount = package.max_price

	# Apply discount
	final_amount = original_amount - (original_amount * discount / 100)

	if request.method == 'POST':
		payment = Payment.objects.create(
			user=request.user,
			package=package,
			original_amount=original_amount,
			discount_percent=discount,
			final_amount=final_amount,
			status=Payment.COMPLETED # simulated payment
		)
		#payment.mark_completed()
		#return redirect('payments:success', payment.id)
		return redirect('subscriptions:my_subscription') #, payment_id=payment.id)
	context = {
		'package': package,
		'original_amount': original_amount,
		'discount': discount,
		'final_amount': final_amount,
		'subscription': subscription,
	}

	return render(request, 'payments/checkout.html', context)




@login_required
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'payments/payment_success.html', {'payment': payment})




@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
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
		plan = request.session.get('subscription_plan')
		subscription, _ = Subscription.objects.get_or_create(user=request.user)
		
		now = timezone.now()
		if subscription.expires_at and subscription.expires_at > now:
			subscription.expires_at +=  timedelta(days=30)
		else:
			subscription.expires_at = now + timedelta(days=30)

		subscription.plan = plan
		subscription.started_at = now
		subscription.save()

		payment.mark_completed()

		return redirect('subscriptions:my_subscription')


	return render(request, 'payments/subscription_checkout.html', {
		'payment': payment
	})
