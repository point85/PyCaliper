from distutils.core import setup

setup(
    name = "PyCaliper",
    packages = ["PyCaliper"],
    version = "1.0.0",
    description = "Units of measure library for Python",
    author = "Kent Randall",
    author_email = "point85.llc@gmail.com",
    # url = "http://chardet.feedparser.org/",
    # download_url = "http://chardet.feedparser.org/download/python3-chardet-1.0.1.tgz",
    keywords = ["units", "measurement units", "units of measure", "python", "uom", "units of measurement", "measurement conversion"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: Released",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Units of Measurement :: Quantity Arithmetic",
        ],
    long_description = 
	"""\
	The Caliper library project manages units of measure and conversions between them.  Caliper is designed to be lightweight and simple to use, yet comprehensive.  It includes a large number of pre-defined units of measure commonly found in science, engineering, technology, finance and the household.  These recognized systems of measurement include the International System of Units (SI), International Customary, United States and British Imperial.  Custom units of measure can also be created in the Caliper unified measurement system.  Custom units are specific to a trade or industry such as industrial packaging where units of can, bottle, case and pallet are typical.  Custom units can be added to the unified system for units that are not pre-defined.  The Caliper library is also available in java and C# at https://github.com/point85/Caliper and CaliperSharp.

	A Caliper measurement system is a collection of units of measure where each pair has a linear relationship, i.e. y = ax + b where 'x' is the abscissa unit to be converted, 'y' (the ordinate) is the converted unit, 'a' is the scaling factor and 'b' is the offset.  In the absence of a defined conversion, a unit will always have a conversion to itself.  A bridge unit conversion is defined to convert between the fundamental SI and International customary units of mass (i.e. kilogram to pound mass), length (i.e. metre to foot) and temperature (i.e. Kelvin to Rankine).  These three bridge conversions permit unit of measure conversions between the two systems.  A custom unit can define any bridge conversion such as a bottle to US fluid ounces or litres.

	"""
)