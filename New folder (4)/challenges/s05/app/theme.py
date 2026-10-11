
from markupsafe import Markup, escape

ASCII_LOGO = r"""
  ____  ____  _____ ____ _____ ____      _    _
 / ___||  _ \| ____/ ___|_   _|  _ \    / \  | |
 \___ \| |_) |  _|| |     | | | |_) |  / _ \ | |
  ___) |  __/| |__| |___  | | |  _ <  / ___ \| |___
 |____/|_|   |_____\____| |_| |_| \_\/_/   \_\_____|
              B Y T E S
"""

CSS = """
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    padding: 35px 20px;
    background: #080d12;
    color: #d5e8e1;
    font-family: Consolas, monospace;
}
.terminal {
    max-width: 900px;
    margin: auto;
    padding: 30px;
    background: #101a20;
    border: 1px solid #32d583;
    border-radius: 10px;
    box-shadow: 0 0 35px #32d58315;
}
.logo {
    color: #32d583;
    font-size: clamp(7px, 1.65vw, 13px);
    overflow-x: auto;
    line-height: 1.15;
}
h1, h2 { color: #32d583; }
.subtitle { color: #88a99d; }
a { color: #63e6be; }
input, button {
    padding: 12px;
    margin: 8px 0;
    background: #0b1117;
    border: 1px solid #367c64;
    color: #ffffff;
    font: inherit;
}
button { cursor: pointer; }
button:hover { background: #18533e; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; }
.error { color: #ff7777; }
</style>
"""

def page(title, content):
    return Markup(
        "<!doctype html><html lang='en'><head>"
        "<meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>{}</title>{}</head><body>"
        "<main class='terminal'><pre class='logo'>{}</pre>"
        "<p class='subtitle'>SPECTRALBYTES // OPERATION GHOST PACKET</p>"
        "<p>[ STAGE 05 - BROKEN OBJECT AUTHORIZATION ]</p>"
        "<hr>{}</main></body></html>"
    ).format(escape(title), Markup(CSS), escape(ASCII_LOGO), Markup(content))
