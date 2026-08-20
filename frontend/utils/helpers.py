import os

CSS_PATH = os.path.join(os.path.dirname(__file__), "..", "styles", "main.css")


def load_css():
    with open(CSS_PATH) as f:
        return f.read()


STRIP_HASH_JS = """
<script>
(function(){
    function strip(){
        if(window.location.hash){
            history.replaceState(null, '', window.location.pathname + window.location.search);
        }
    }
    strip();
    window.addEventListener('hashchange', strip);
    setTimeout(strip, 500);
    setTimeout(strip, 1500);
})();
</script>
"""

LIGHT_THEME_SCRIPT = '<script>document.documentElement.setAttribute("data-theme","light");</script>'
DARK_THEME_SCRIPT = '<script>document.documentElement.removeAttribute("data-theme");</script>'
