import locale
import gettext

##
# The Localizer class provides localization services for unit of measure names, symbols and descriptions as well as error messages.
#
class Localizer:  
    # root folder 
    localePath = "locales"
     
    # single instance
    localizerInstance = None
    
    def __init__(self):
        Localizer.localizerInstance = self
        self.messages = None
        self.units = None
                    
    @staticmethod
    def instance():
        if (Localizer.localizerInstance is None):
            Localizer()
        return Localizer.localizerInstance 
    
    @staticmethod
    def getLC():
        # get the default locale and the language code
        thisLocale = locale.getdefaultlocale()
        langCC = thisLocale[0]
        return langCC
    
    ##
    # Get the translated error message text for the default locale and country code 
    # 
    # @param msgId Message identifier
    # @return translated text    
    def messageStr(self, msgId):
        if (self.messages is None):
            # translated text with error messages for this locale and country code
            self.messages = gettext.translation("messages", localedir=Localizer.localePath, languages=[Localizer.getLC()])
            self.messages.install()
            
        # Get an error message by its id
        return self.messages.gettext(msgId)
    
    ##
    # Get the translated user-visible text for the default locale and country code 
    # 
    # @param msgId Message identifier
    # @return translated text  
    def langStr(self, msgId):        
        if (self.units is None):
            # translated user-visible text for this locale  and country code
            self.units = gettext.translation("units", localedir=Localizer.localePath, languages=[Localizer.getLC()])
            self.units.install()
        
        # Get a unit name, symbol or description by its id
        return self.units.gettext(msgId)
