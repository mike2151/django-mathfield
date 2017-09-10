from __future__ import unicode_literals
import six
from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
import textwrap
import json
import cgi

if six.PY3:
    import cgi as html
    basestring = str

class MathFieldWidget(forms.Textarea):
    
    def render(self, name, value, attrs=None):
        
        try:
            value = json.loads(value)
            raw_value = value['raw']
        except (json.JSONDecodeError, TypeError):
            raw_value = ''

        output = super(MathFieldWidget, self).render(name, raw_value, attrs)
        output = '<div id="{0}-container"><span>{1}</span></div>'.format(
            attrs['id'], output)

        if value:
            if isinstance(value, dict):
                raw = value['raw'] if 'raw' in value else ''
                html = value['html'] if 'html' in value else ''
                html = html.replace("'", "\'")
            elif isinstance(value, basestring):
                raw = value
                html = ''
            raw = cgi.escape(raw.replace('\\', '\\\\'))
        else:
            raw = html = ''

        # Escape new lines
        raw = raw.replace('\n', '\\n')

        # Escape HTML
        html = cgi.escape(html)

        if hasattr(settings, 'STATIC_URL'):
            static_url = getattr(settings, 'STATIC_URL', {})
        else:
            static_url = '/static/'
        output += textwrap.dedent("""
            <link rel="stylesheet" type="text/css" 
                href="{static}mathfield/css/mathfield.css"/>
            <script type="text/javascript" 
                src="{static}mathfield/js/katex.min.js"></script>
            <script type="text/javascript" 
                src="{static}mathfield/js/mathfield.min.js"></script>
            <script type="text/javascript" 
                src="{static}mathfield/js/mathfield_admin.js"></script>
            <script type="text/javascript">
                renderMathFieldForm("{id}", "{raw}");
            </script>
        """.format(static=static_url, id=attrs['id'], raw=raw))

        return mark_safe(output)