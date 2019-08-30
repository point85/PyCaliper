
import locale
import gettext

class Localizer:    
    # single instance
    localizer = None
    
    def __init__(self):
        Localizer.localizer = self
        self.messages = None
        self.units = None
                    
    @staticmethod
    def instance():
        if (Localizer.localizer is None):
            Localizer()
        return Localizer.localizer 
    
    @staticmethod
    def getLC():
        # get the default locale and the language code
        thisLocale = locale.getdefaultlocale('LANG)')
        langCC = thisLocale[0]
        #return langCC[0:2]
        return langCC
        
    def messageStr(self, msgId):
        if (self.messages is None):
            # translated text with error messages for this locale and country code
            self.messages = gettext.translation('messages', localedir='locales', languages=[Localizer.getLC()])
            self.messages.install()
            #_M = self.messages.gettext
            
        # Get an error message by its id
        return self.messages.gettext(msgId)
    
    def unitStr(self, msgId):
        if (self.units is None):
            # translated user-visible text for this locale  and country code
            self.units = gettext.translation('units', localedir='locales', languages=[Localizer.getLC()])
            self.units.install()
                #_U = self.units.gettext
        
        # Get a unit name, symbol or description by its id
        return self.units.gettext(msgId)