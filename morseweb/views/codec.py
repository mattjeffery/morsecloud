import urllib
import urllib2
import logging
import tempfile
import aifc
import wave

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
def encode(request, ext='aiff'):
    """Generate some morse!
    """
    ext = ext.lstrip('.')
    if ext in ('aiff', 'aif'):
        opener = aifc
    elif ext in ('wave', 'wav'):
        opener = wave
    else:
        raise ValueError('Filetype {0} not supported'.format(ext))
    msg_text = request.POST.get('text') or request.GET.get('text', 'sos')

    # store the audio in memory
    strio_out = StringIO()

    # write the audio
    m = morseweb.morsecodec.morseCodec()
    mime_type = m.text2audio(msg_text, strio_out, customWriter=opener, closeWriter=False)
    if not mime_type:
        mime_type = 'audio/x-aiff'

    # seek to the begining of the file
    strio_out.seek(0)

    # output the audio
    return Response(strio_out.read(), content_type=mime_type)

@view_config(route_name='soundcloud_upload', renderer='jsonp')
def encode_upload(request):
    """encode a message and upload it to soundcloud
    """
    
    missing = []

    msg_text = request.POST.get('text') or request.GET.get('text')
    oauth_token = request.POST.get('access_token') or request.GET.get('access_token')
    title = request.POST.get('title') or request.GET.get('title')

    if not msg_text:
        missing.append('text')

    if not oauth_token:
        missing.append('access_token')

    if not title:
        missing.append('title')

    if len(missing) > 0:
        return { 'success': False,
                 'error': { 'msg': 'missing arguments: {0}'.format(missing),
                            'code': 400 } }

    # store the audio in memory
    strio_out = StringIO()

    # write the audio
    m = morseweb.morsecodec.morseCodec()
    mime_type = m.text2audio(msg_text, strio_out, customWriter=wave, closeWriter=False)
    if not mime_type:
        mime_type = 'audio/x-aiff'

    # seek to the begining of the file
    strio_out.seek(0)

    params = {'oauth_token': oauth_token,
              'track': { 'asset_data': strio_out.read(),
                         'title': title,
                         'sharing': 'public'} }

    try:
        urlfh = urllib2.urlopen("https://api.soundcloud.com/tracks.json",
                                urllib.urlencode(params))
    except urllib2.HTTPError as exc:
        return { 'success': False,
                 'error': { 'msg': 'failed with error code: {0}'.format(exc.code),
                            'code': exc.code } }

    # output the audio
    return simplejson.load(urlfh)

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
