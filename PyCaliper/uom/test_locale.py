
import locale
from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.unit_type import UnitType
"""
gettext.bindtextdomain('test_locale', localedir='locales')
gettext.textdomain('test_locale')
_ = gettext.gettext
"""

"""
# get the default locale and the language code
thisLocale = locale.getdefaultlocale('LANG)')
langCC = thisLocale[0]

# translated text for this locale
messages = gettext.translation('test_locale', localedir='locales', languages=[langCC[0:2]])
messages.install()
_ = messages.gettext
"""

"""
def print_some_strings():
    print(_("Hello world"))
    print(_("This is a translatable string"))
    print(_("must.be.same.as"))
    print(_("amount.cannot.be.null"))
"""    
def raw_strings():
    #print ("Hi ! My name is {} and I am {} years old".format("User", 19)) 
    #my_string = "{}, is a {} {} science portal for {}"
    #print ("Hello")
    #print (my_string)
    #print("what is wrong")
    #formatted = my_string.format( "GeeksforGeeks", "computer", "geeks", "too" )
    #print (formatted)
    a = 1
    print(a)

"""
def another():
    print ("Hi ! My name is {} and I am {} years old".format("User", 19))
    s = _("must.be.same.as")
    args = "one", "two", "three", "four"
    print (s.format(*args))
"""
 
if __name__=='__main__':
    sys = MeasurementSystem.instance()
    tm = sys.getTypeMap(UnitType.VELOCITY)
    
    __MULT = '\xB7'
    print(__MULT)
    
    #msg = MeasurementSystem.getMessage("must.be.same.as")
    #print(msg)
        
    myLocale = locale.getdefaultlocale('LANG)')
    langCC = myLocale[0]
    lang = langCC[0:2]
    
    #text = messages.gettext("must.be.same.as")
    
    #print_some_strings()
    #raw_strings()
    #another()
    print ("end")
    