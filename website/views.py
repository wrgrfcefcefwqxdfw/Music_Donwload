# website routes
from flask import Blueprint, render_template, request, jsonify, flash, url_for, redirect
from flask_login import login_required, current_user
from .models import Note
from dotenv import load_dotenv
from . import db
from .validateLink import validate_youtube_link
import json, os, stripe
from pytube import YouTube

load_dotenv()
views = Blueprint('views', __name__)
stripe.api_key = os.getenv('STRIPE_PRIVATE_KEY')

@views.route('/', methods=['GET', 'POST'])
# cannot go to the homepage unless u are logged in
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
    # to render home.html user render_template
    # pass user variable which is the current user
    return render_template("home.html", user=current_user)

@views.route('/videos', methods=['GET', 'POST'])
@login_required
def videos():
    if request.method == 'POST':
        url = request.form['vid']
        segments = url.split("=")
        value = segments[-1]
        new_url = "video_url"+value
    else:
        new_url=""
    # to render home.html user render_template
    # pass user variable which is the current user
    return render_template("videos.html", user=current_user, video_link=new_url)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/downloader', methods=['GET', 'POST'])
@login_required
def downloader():
    if request.method == 'POST':
        ytlink = request.form['ytlink']
        if validate_youtube_link(ytlink):
            try:
                path = os.getcwd()
                full_path = os.path.join(path, 'static/downloaded')
                if ytlink.startswith("https://youtu.be/"):
                    segments = ytlink.split("/")
                    # Get the last segment of the URL
                    video_id = segments[-1]
                    ytlink = "https://www.youtube.com/watch?v=" + video_id

                print(ytlink)
                yt = YouTube(ytlink)
                ytTitle = yt.title[:10]
                print(ytTitle)
                title = ytTitle + '.mp3'
                stream = yt.streams.get_audio_only()
                print(full_path)
                stream.download(output_path=full_path, filename=title)

                flash(f'Download Complete', category='success')
                return redirect(url_for("download_file", filename=title))

            except Exception as e:
                flash("Unexpected Error", category='error')
                print(f'Error: {e}')
        else:
            flash("Not a valid youtube link", category='error')
    # to render home.html user render_template
    # pass user variable which is the current user
    return render_template("downloader.html", user=current_user)


@views.route('/checkout')
def checkout():
    return render_template("checkout.html")

@views.route('/success')
def success():
    return render_template("success.html")

@views.route('/cancel')
def cancel():
    return render_template("cancel.html")

@views.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1NOiyFLDy6PYosgFb7tjskQ2',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:5000' + '/success',
            cancel_url='http://localhost:5000'
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)
# above
# it is going to take in some data from a post
# request, it's going to load it as a Jason object or a Python dictionary we're then going to access the note ID attribute,
# which again, it's right here. What we'll do then is we'll say, note doc query dot gets we'll look for the note
# that has that ID check. If it exists, first of all, if it does exist, then, um, of course we can delete it. If it doesn't, we don't need
# to delete it. And then what we'll do is we'll say, well, if we own this notes with the user who is signed in,
# does actually own this note, because we don't want to let users who are assigned in delete other people's notes, right? Uh, then we will
# delete the notes. And then what we'll do is we'll return an empty response. Now we just
# need to do this because we do need to return something from these views. We're not returning HTML here. We're just returning an
# empty response that is either saying, Hey, you know, it was successful or it didn't work
