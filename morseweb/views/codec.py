import urllib2
import logging
import tempfile

import morseweb.morsecodec
from StringIO import StringIO

import pyramid.security
import pyramid.settings

from pyramid.response import Response
from pyramid.view import view_config

from ..models import DBSession
from ..models.user import User

from . import json_request

log = logging.getLogger(__name__)

@view_config(route_name='encode')
def encode(request):
    """Generate some morse!
    """

    msg_text = request.POST.get('text') or request.GET.get('text', 'sos')

    # store the audio in memory
    strio_out = StringIO()

    # write the audio
    m = morseweb.morsecodec.morseCodec()
    m.text2audio(msg_text, strio_out, closeWriter=False)

    mime_type = 'audio/x-aiff'

    # seek to the begining of the file
    strio_out.seek(0)

    # output the audio
    return Response(strio_out.read(), content_type=mime_type)

@view_config(route_name='soundcloud_upload')
def encode_upload(request):
    pass

    
@view_config(route_name='decode', renderer='jsonp')
def decode(request):
    """Decode some morse!
    """
    settings = pyramid.settings.get_settings()
    client_id = settings['soundcloud.client.id']

    track_id = request.GET.get('track_id') or request.POST.get('track_id')
    if not track_id:
        return { "error": { "code": "400",
                            "msg": "missing track_id argument" },
                 "success": False }

    else:
        track = json_request("http://api.soundcloud.com/tracks/{0}.json".format(track_id),
                             { 'client_id': client_id })

        dlurl = track.get('download_url')+'?client_id='+client_id

        log.debug("Track to download: {0}".format(dlurl))

        _, mp3path = tempfile.mkstemp(prefix='mp3-morse-', suffix='.mp3')

        mp3content = urllib2.urlopen(dlurl).read()

        with open(mp3path, 'wb') as mp3file:
            mp3file.write(mp3content)

        m = morseweb.morsecodec.morseCodec()
        msg = m.audio2text(mp3path)

        #todo delete file

        return { "response": { "message": msg },
                 "success": True }
