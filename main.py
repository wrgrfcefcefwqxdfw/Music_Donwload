# __init__.py allows you to import website as package
from website import create_app
from flask import send_from_directory, render_template, request, url_for, abort
import os, stripe

app = create_app()
app.config["UPLOAD_FOLDER"] = "static/downloaded"
# app.config['STRIPE_PUBLIC_KEY'] = 'YOUR_STRIPE_PUBLIC_KEY'
# app.config['STRIPE_SECRET_KEY'] = 'YOUR_STRIPE_SECRET_KEY'
#
# stripe.api_key = app.config['STRIPE_SECRET_KEY']


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    path = os.getcwd()
    uploads = os.path.join(path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, path=filename, as_attachment=True)


# @app.route('/checkout')
# def checkout():
#     '''
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[{
#             'price': 'price_1GtKWtIdX0gthvYPm4fJgrOr',
#             'quantity': 1,
#         }],
#         mode='payment',
#         success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
#         cancel_url=url_for('index', _external=True),
#     )
#     '''
#     return render_template(
#         'checkout.html',
#         # checkout_session_id=session['id'],
#         # checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
#     )
#
#
# @app.route('/stripe_pay')
# def stripe_pay():
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[{
#             'price': 'YOUR_PRODUCT_PRICE_ID',
#             'quantity': 1,
#         }],
#         mode='payment',
#         success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
#         cancel_url=url_for('checkout', _external=True),
#     )
#     return {
#         'checkout_session_id': session['id'],
#         'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
#     }
#
#
# @app.route('/thanks')
# def thanks():
#     return render_template('success.html')
#
#
# @app.route('/stripe_webhook', methods=['POST'])
# def stripe_webhook():
#     print('WEBHOOK CALLED')
#
#     if request.content_length > 1024 * 1024:
#         print('REQUEST TOO BIG')
#         abort(400)
#     payload = request.get_data()
#     sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
#     endpoint_secret = 'YOUR_ENDPOINT_SECRET'
#     event = None
#
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         print('INVALID PAYLOAD')
#         return {}, 400
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         print('INVALID SIGNATURE')
#         return {}, 400
#
#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         print(session)
#         line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
#         print(line_items['data'][0]['description'])
#
#     return {}


if __name__ == '__main__':
    app.run(debug=True)
