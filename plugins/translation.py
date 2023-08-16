import os
from config import *
import re

class Translation:
  START_TXT = """<b>Hai {}!!</b>
<i>I'm Simple Auto file Forward & IMDb Search Bot
This Bot forward all files to One Public channel to Your Personal channel
More details /help</i>"""
  CAPTION = "`{}`\n\n" + str(CAPTION)
  HELP_TXT = """<b>Follow These Steps!!</b>
<b>• Currectly fill your Heroku Config vars</b> <code>FROM_CHANNEL</code> and <code>TO_CHANNEL</code> <b>and other Vars</b>
<b>• Then give admin permission in your personal telegram channel</b>
<b>• Then send any message In your personal telegram channel</b>
<b>• Then use /run command in your bot</b>
<b>◉ I can search IMDb Just in a second. wanna try just type: $<Movie Name>&</b>
<b>@filmykeedha</b>

<b><u>Available Command</b></u>

* /start - <b>Bot Alive</b>
* /help - <b>more help</b>
* /run - <b>start forward</b>
* /about - <b>About Me</b>"""
  ABOUT_TXT = """<b><u>My Info</b></u>

<b>Name :</b> <code>Auto File Forword Bot</code>
<b>Credit :</b> <code>@Filmykeedha & PANKAJ</code>
<b>Language :</b> <code>Python3</code>
<b>Library :</b> <code>Pyrogram v1.2.9</code>
<b>Server :</b> <code>Heroku</code>
<b>Build :</b><code>V0.1</code>"""
  
