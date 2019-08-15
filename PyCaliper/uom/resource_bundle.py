import gettext
_ = gettext.gettext

class ResourceBundle:        
    def __init__(self, name : str):
        self.domain = name
        gettext.bindtextdomain(name, "/PyCaliper/PyCaliper/uom/locales")
        # gettext.textdomain(name)
        
    def getString(self, msgid: str) -> str:
        return gettext.dgettext(self.domain, msgid)