##
# The Localizer class provides localization services for unit of measure names, symbols and descriptions as well as error messages.
#
import locale
import gettext
import threading
import os
from pathlib import Path
from functools import lru_cache

class Localizer:
    """Thread-safe singleton for handling localization."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.messages = None
        self.units = None
        self.localePath = Path(__file__).parent / "locales"
        self._language_code = None  # Cache the language code
    
    @staticmethod
    def instance():
        return Localizer()
    
    @staticmethod
    @lru_cache(maxsize=1)
    def getLC():
        """Get language code with robust fallback (cached)."""
        try:
            current_locale = locale.getlocale()[0]
            if current_locale:
                return current_locale
        except (locale.Error, ValueError):
            pass
        
        # Check environment variables
        for var in ('LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'):
            if var in os.environ and os.environ[var]:
                return os.environ[var].split(':')[0]
        
        return 'en_US'
    
    def messageStr(self, msgId):
        """Get translated error message."""
        if self.messages is None:
            try:
                self.messages = gettext.translation(
                    "messages",
                    localedir=str(self.localePath),
                    languages=[self.getLC(), 'en_US'],
                    fallback=True
                )
            except Exception as e:
                print(f"Warning: Could not load message translations: {e}")
                self.messages = gettext.NullTranslations()
        
        try:
            return self.messages.gettext(msgId)
        except Exception:
            return msgId
    
    def langStr(self, msgId):
        """Get translated unit text."""
        if self.units is None:
            try:
                self.units = gettext.translation(
                    "units",
                    localedir=str(self.localePath),
                    languages=[self.getLC(), 'en_US'],
                    fallback=True
                )
            except Exception as e:
                print(f"Warning: Could not load unit translations: {e}")
                self.units = gettext.NullTranslations()
        
        try:
            return self.units.gettext(msgId)
        except Exception:
            return msgId