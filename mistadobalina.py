#!/usr/bin/python
"""
A script that selects two random lines from Del Tha Funkee Homosapien's first album,
I Wish My Brother George Was Here, and posts them to the @mistadoblina Twitter account.

http://twitter.com/mistadobalina

Lyrics data provied by LyricWiki. Their API is documented here: 
* http://lyricwiki.org/LyricWiki:SOAP

Dependencies: PyXML, fpconst, SOAPpy, python-twitter, simplejson.

For more information on SOAPpy or python-twitter refer to:
* http://www.diveintopython.org/soap_web_services/
* http://code.google.com/p/python-twitter/

The MIT License
 
Copyright (c) 2008 Ben Welsh
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

__author__ = "Ben Welsh <palewire@palewire.com>"
__date__ = "$Date: 2008/06/01 $"
__version__ = "$Revision: 0.2 $"


import re
import cgi
import random
import string
import twitter
from SOAPpy import WSDL 

# Since the LyricWiki getArtist() method wasn't working, I just hammered in the song titles by hand.
# I've excluded a couple tracks. Here's why: 
# * "Interlude" is too short to include, I figure. 
# * There weren't good lyrics in the API for "The Wacky World of Public Transit"
I_Wish_My_Brother_George_Was_Here = ['Dr._Bombay', 'What_Is_A_Booty', 'Ahonetwo,_Ahonetwo', 'Mistadobalina', 
                                     'Sleepin\'_On_My_Couch', 'Sunny_Meadowz', 'Eye Examination', 
                                     'Pissin\'_On_Your_Steps', 'Dark Skin Girls', 'Money_For_Sex', 
                                     'Hoodz_Come_In_Dozens', 'Same_Ol\'_Thing', 'Ya_Li\'l_Crumbsnatchers']

# Selecting a random song from the album
random_song = random.randrange(len(I_With_My_Brother_George_Was_Here))
song = I_Wish_My_Brother_George_Was_Here[random_song]

# Logging into the LyricWiki API and downloading our randomly selected song
wsdlFile = ('http://lyricwiki.org/server.php?wsdl')
server = WSDL.Proxy(wsdlFile)
song = server.getSong('Del_Tha_Funkee_Homosapien', song)
title = song[1]
lyrics = song[2]
lines = string.split(lyrics, '\n')

def Filter(text):
    """Flagging any line that contains one of the words we want to omit."""
    
    # The words we want to exclude.
    black_list = ('Chorus', 'CHORUS', 'REPEAT', 'BRIDGE', 
                  'PAUSE', 'INTERLUDE', 'CHROUS', 'Chrous', 
                  'chorus', 'REPEAT', 'Bridge', 'Intro', 
                  'Verse One', 'Verse Two', '&(.*);')
    
    # Walk through each term in the list and return false where there's a match.
    # There must be a more concise way to do this with a comprehension, but I haven't 
    # figured it out yet.
    for term in black_list:
         if re.search(term, line): 
              return False
         else: 
              pass
    return True

# Walking every line in the song through the filter.
# If they don't have a blacklisted word, they return True and we keep em.    
lines = [line for line in lines if Filter(line)]

# Selecting a random line from the song
random_line = random.randrange(len(lines))

# Since there's a chance we might draw the last line in the song, 
# the exception should back it up to grab the second to last line.
try:
    quote = lines[random_line] + ' / ' + lines[random_line+1]
except:
    quote = lines[random_line-1] + ' / ' + lines[random_line]

# Shooting it up to Twitter
# This could probably use some test that makes sure the quote isn't over Twitters 140 character limit.
# But I'm too lazy to do that tonight. 
un = 'mistadobalina'
pw = '#####'
api = twitter.Api(username=un, password=pw)
status = api.PostUpdate(quote)



