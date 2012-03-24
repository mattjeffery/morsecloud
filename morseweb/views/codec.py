import morseweb.morsecodec
from StringIO import StringIO

import pyramid.security

from pyramid.response import Response
from pyramid.view import view_config

from ..models import DBSession
from ..models.user import User


@view_config(route_name='encode')
def encode(request):
    """Generate some morse!
    """

    msg_text = request.POST.get('text') or request.GET.get('text', 'sos')

    # store the audio in memory
    strio_out = StringIO()

    # write the audio
    m = morseweb.morsecodec.morseCodec()
    mime_type = m.text2audio(msg_text, strio_out, closeWriter=False)

    mime_type = 'audio/x-aiff'

    # seek to the begining of the file
    strio_out.seek(0)

    # output the audio
    return Response(strio_out.read(), content_type=mime_type)

@view_config(route_name='decode', renderer='jsonp')
def decode(request):
    """Decode some morse!
    """

    return { "error": { "code": "400",
                        "msg": ":(" } }
