# PyCaliper
The PyCaliper library project manages units of measure and conversions between them.  PyCaliper is designed to be lightweight and simple to use, yet comprehensive.  It includes a large number of pre-defined units of measure commonly found in science, engineering, technology, finance and the household.  These recognized systems of measurement include the International System of Units (SI), International Customary, United States and British Imperial.  Custom units of measure can also be created in the PyCaliper unified measurement system.  Custom units are specific to a trade or industry such as industrial packaging where units of can, bottle, case and pallet are typical.  Custom units can be added to the unified system for units that are not pre-defined.  The PyCaliper library is also available in Java at https://github.com/point85/Caliper and in C# at https://github.com/point85/CaliperSharp.

A PyCaliper measurement system is a collection of units of measure where each pair has a linear relationship, i.e. y = ax + b where 'x' is the abscissa unit to be converted, 'y' (the ordinate) is the converted unit, 'a' is the scaling factor and 'b' is the offset.  In the absence of a defined conversion, a unit will always have a conversion to itself.  A bridge unit conversion is defined to convert between the fundamental SI and International customary units of mass (i.e. kilogram to pound mass), length (i.e. metre to foot) and temperature (i.e. Kelvin to Rankine).  These three bridge conversions permit unit of measure conversions between the two systems.  A custom unit can define any bridge conversion such as a bottle to US fluid ounces or litres.
 
## Concepts
 
All units are owned by the unified measurement system. Units 'x' and 'y' belong to a relational system (such as SI or International Customary).  Units 'w' and 'z' belong to a second relational system.  Unit 'y' has a linear conversion to unit 'x'; therefore 'x' must be defined before 'y' can be defined.  Unit 'x' is also related to 'y' by x = (y - b)/a.  Unit 'w' has a conversion to unit 'z'.  Unit 'z' is related to itself by z = z + 0. Unit 'x' has a bridge conversion defined to unit 'z' (for example a foot to a metre).  Note that a bridge conversion from 'z' to 'x' is not necessary since it is the inverse of the conversion from 'x' to 'z'.
 
*Scalar Unit* 

A simple unit, for example a metre, is defined as a scalar UOM.  A special scalar unit of measure is unity or dimensionless "1".  

*Product Unit*

A unit of measure that is the product of two other units is defined as a product UOM.  An example is a Joule which is a Newton·metre.  

*Quotient Unit*  

A unit of measure that is the quotient of two other units is defined as a quotient UOM. An example is a velocity, e.g. metre/second.  

*Power Unit*

A unit of measure that has an exponent on a base unit is defined as a power UOM. An example is area in metre^2. Note that an exponent of 0 is unity, and an exponent of 1 is the base unit itself. An exponent of 2 is a product unit where the multiplier and multiplicand are the base unit.  A power of -1 is a quotient unit of measure where the dividend is 1 and the divisor is the base unit.  

*Type*

Units are classified by type, e.g. length, mass, time and temperature.  Only units of the same type can be converted to one another. Pre-defined units of measure are also enumerated, e.g. kilogram, Newton, metre, etc.  Custom units (e.g. a 1 litre bottle) do not have a pre-defined type or enumeration and are referred to by a unique base symbol.

*Base Symbol*
 
All units have a base symbol that is the most reduced form of the unit.  For example, a Newton is kilogram·metre/second^2.  The base symbol is used in the measurement system to register each unit and to discern the result of arithmetic operations on quantities.  For example, dividing a quantity of Newton·metres by a quantity of metres results in a quantity of Newtons. 

*Quantity*

A quantity is an amount (implemented as a double precision number) together with a unit of measure.  When arithmetic operations are performed on quantities, the original units can be transformed.  For example, multiplying a length quantity in metres by a force quantity in Newtons results in a quantity of energy in Joules (or Newton-metres).

*Product of Powers*

A unit of measure is represented internally as a product of two other power units of measure.  For a simple scalar UOM (e.g. kilogram), both of the UOMs are null with the exponents defaulted to 0.  For a product UOM (e.g. Newton), the first UOM is the multiplier and the second is the multiplicand with both exponents set to 1.  For a quotient UOM (e.g. kilograms/hour), the first UOM is the dividend and the second is the divisor.  The dividend has an exponent of 1 and the divisor an exponent of -1.  For a power UOM (e.g. square metres), the first UOM is the base and the exponent is the power.  In this case, the second UOM is null with the exponent defaulted to 0.

From the two power products, a unit of measure can then be recursively reduced to a map of base units of measure and corresponding exponents along with a scaling factor.  For example, a Newton reduces to (kg, 1), (m, 1), (s, -2) in the SI system.  Multiplying, dividing and converting a unit of measure is accomplished by merging the two maps (i.e. "cancelling out" units) and then computing the overall scaling factor.  The base symbol is obtained directly from the final map.
 
## Code Examples
The singleton unified MeasurementSystem is obtained by calling:
```python
msys = MeasurementSystem.instance()
```

The units.po file in the /locales/<locale>/LC_MESSAGES folder defines the name, symbol and description for each of the predefined units of measure.  The units.po file is localizable.  It is read by a Singleton instance of the Localizer class.For example, 'metres' can be changed to use the US spelling 'meters' or descriptions can be translated to another language by placing the corresponding .mo file in the appropriate locale folder.

The metre scalar UOM is created by the MeasurementSystem as follows:
```python
uom = msys.createScalarUOM(UnitType.LENGTH, Unit.METRE, Localizer.instance().langStr("m.name"), Localizer.instance().langStr("m.symbol"),
    Localizer.instance().langStr("m.desc"))
``` 

The square metre power UOM is created by the MeasurementSystem as follows: 
```python
uom = msys.createPowerUOM(UnitType.AREA, Unit.SQUARE_METRE, Localizer.instance().langStr("m2.name"),
    Localizer.instance().langStr("m2.symbol"), Localizer.instance().langStr("m2.desc"), msys.getUOM(Unit.METRE), 2)
```

The metre per second quotient UOM is created by the MeasurementSystem as follows: 
```python
uom = msys.createQuotientUOM(UnitType.VELOCITY, Unit.METRE_PER_SEC, Localizer.instance().langStr("mps.name"),
    Localizer.instance().langStr("mps.symbol"), Localizer.instance().langStr("mps.desc"), msys.getUOM(Unit.METRE), msys.getSecond())
```

The Newton product UOM is created by the MeasurementSystem as follows: 
```python
uom = msys.createProductUOM(UnitType.FORCE, unit, Localizer.instance().langStr("newton.name"),
    Localizer.instance().langStr("newton.symbol"), Localizer.instance().langStr("newton.desc"), msys.getUOM(Unit.KILOGRAM),
    msys.getUOM(Unit.METRE_PER_SEC_SQUARED))
```

A millisecond is 1/1000th of a second with a defined prefix and created as:

```python 
msec = msys.createPrefixedUOM(Prefix.milli(), msys.getSecond())
```

For a second example, a US gallon = 231 cubic inches:
```python			
uom = msys.createScalarUOM(UnitType.VOLUME, Unit.US_GALLON,
    Localizer.instance().langStr("us_gallon.name"), Localizer.instance().langStr("us_gallon.symbol"), Localizer.instance().langStr("us_gallon.desc"))
    uom.setConversion(231.0, msys.getUOM(Unit.CUBIC_INCH), 0.0)
```

When creating the foot unit of measure in the unified measurement system, a bridge conversion to metre is defined (1 foot = 0.3048m):
```python
uom = msys.createScalarUOM(UnitType.LENGTH, Unit.FOOT, Localizer.instance().langStr("foot.name"),
    Localizer.instance().langStr("foot.symbol"), Localizer.instance().langStr("foot.desc"))
    
    # bridge to SI
    uom.setBridgeConversion(0.3048, self.getUOM(Unit.METRE), 0.0)
```

Custom units of measure (with no pre-defined Unit) and conversions can also be created:
```python
# gallons per hour
gph = msys.createQuotientUOM(UnitType.VOLUMETRIC_FLOW, None, "gph", "gal/hr", "gallons per hour", 
    msys.getUOM(Unit.US_GALLON), msys.getHour())

# 1 16 oz can = 16 fl. oz.
one16ozCan = msys.createScalarUOM(UnitType.VOLUME, None, "16 oz can", "16ozCan", "16 oz can")
one16ozCan.setConversion(16.0, msys.getUOM(Unit.US_FLUID_OUNCE))

# 400 cans = 50 US gallons
q400 = Quantity(400.0, one16ozCan)
q50 = q400.convert(msys.getUOM(Unit.US_GALLON))

# 1 12 oz can = 12 fl.oz.
one12ozCan = msys.createScalarUOM(UnitType.VOLUME, None, "12 oz can", "12ozCan", "12 oz can")
one12ozCan.setConversion(12.0, msys.getUOM(Unit.US_FLUID_OUNCE))

# 48 12 oz cans = 36 16 oz cans
q48 = Quantity(48.0, one12ozCan)
q36 = q48.convert(one16ozCan)

# 6 12 oz cans = 1 6-pack of 12 oz cans
sixPackCan = msys.createScalarUOM(UnitType.VOLUME, None, "6-pack", "6PCan", "6-pack of 12 oz cans")
sixPackCan.setConversion(6.0, one12ozCan)    

# 1 case = 4 6-packs
fourPackCase = msys.createScalarUOM(UnitType.VOLUME, None, "6-pack case", "4PCase", "four 6-packs")
fourPackCase.setConversion(4.0, sixPackCan)
        
# A beer bottling line is rated at 2000 12 ounce cans/hour (US) at the
# filler. The case packer packs four 6-packs of cans into a case.
# Assuming no losses, what should be the rating of the case packer in
# cases per hour? And, what is the draw-down rate on the holding tank
# in gallons/minute?
canph = msys.createUnclassifiedQuotientUOM(one12ozCan, msys.getHour())
caseph = msys.createUnclassifiedQuotientUOM(fourPackCase, msys.getHour())
gpm = msys.createUnclassifiedQuotientUOM(msys.getUOM(Unit.US_GALLON), msys.getMinute())
        
# filler production rate
filler = Quantity(2000.0, canph)

# tank draw-down
draw = filler.convert(gpm)

# case packer production
packer = filler.convert(caseph)
```

Quantities can be added, subtracted and converted:
```python
m = msys.getUOM(Unit.METRE)
cm = msys.createPrefixedUOM(Prefix.centi(), m)
        
q1 = Quantity(2.0, m)
q2 = Quantity(2.0, cm)
        
# add two quantities.  q3 is 2.02 metre
q3 = q1.add(q2)
        
# q4 is 202 cm
q4 = q3.convert(cm)
        
# subtract q1 from q3 to get 0.02 metre
q3 = q3.subtract(q1)
```

as well as multiplied and divided:
```python
q1 = Quantity(50.0, cm)
q2 = Quantity(50.0, cm)
        
# q3 = 2500 cm^2
q3 = q1.multiply(q2)
        
# q4 = 50 cm
q4 = q3.divide(q1)
```

and inverted:
```python
mps = msys.getUOM(Unit.METRE_PER_SEC) 
q1 = Quantity(10.0, mps)
        
# q2 = 0.1 sec/m
q2 = q1.invert()
```

To make working with linearly scaled units of measure (with no offset) easier, the MeasurementSystem's createPrefixedUOMUOM() method that uses a Prefix can be used.  This method accepts a Prefix enum and the unit of measure that it is scaled against.  The resulting unit of measure has a name concatented with the Prefix's name and target unit name.  The symbol is formed similarly.  For example, a centilitre (cL) is created from the pre-defined litre by:
```python
litre = msys.getUOM(Unit.LITRE)
cL = msys.createPrefixedUOM(Prefix.centi(), litre)
```
and, a megabyte (MB = 2^20 bytes) is created by:
```python
mB = msys.createPrefixedUOM(Prefix.mebi(), msys.getUOM(Unit.BYTE))
```

*Implicit Conversions*

A quantity can be converted to another unit of measure without requiring the target UOM to first be created.  If the quantity has a product or quotient UOM, use the convertToPowerProduct() method.  For example:

```python
# convert 1 newton-metre to pound force-inches
nmQ = Quantity(1.0, msys.getUOM(Unit.NEWTON_METRE))
lbfinQ = nmQ.convertToPowerProduct(msys.getUOM(Unit.POUND_FORCE), msys.getUOM(Unit.INCH))
```

If the quantity has power UOM, use the convertToPower() method.  For example:

```python
# convert 1 square metre to square inches
m2Q = Quantity(1.0, msys.getUOM(Unit.SQUARE_METRE))
in2Q = m2Q.convertToPower(msys.getUOM(Unit.INCH))
```

Other UOMs can be converted using the convert() method.

*Classification*

During arithmetic operations, the final type of the unit may not be known.  In this case, invoking the classify() method will attempt to find a matching unit type.  For example, the calculated unit of measure below has a type of UnitType.ELECTRIC_CAPACITANCE:

```python
s = msys.getSecond()
m = msys.getUOM(Unit.METRE)
kg = msys.getUOM(Unit.KILOGRAM)
amp = msys.getUOM(Unit.AMPERE)
sm3 = msys.createUnclassifiedPowerUOM(s, -3)
am2 = msys.createUnclassifiedPowerUOM(amp, -2)
m2 = msys.createUnclassifiedPowerUOM(m, 2)
        
cap = sm3.multiply(am2).multiply(m2).divide(kg).classify()
```

A quantity resulting from an arithmetic operation can also be classified.  For example, the "density" quantity has UnitType.DENSITY:

```python
mass = Quantity(1035, msys.getUOM(Unit.KILOGRAM))
volume = Quantity(1000, msys.getUOM(Unit.LITRE))
density = mass.divide(volume).classify()
```

## Physical Unit Examples

Water boils at 100 degrees Celcius.  What is this temperature in Fahrenheit?
```python
qC = Quantity(100.0, msys.getUOM(Unit.CELSIUS))
qF = qC.convert(msys.getUOM(Unit.FAHRENHEIT))
```

A nutrition label states the energy content is 1718 KJ.  What is this amount in kilo-calories?
```python
kcal = msys.createPrefixedUOM(Prefix.kilo(), msys.getUOM(Unit.CALORIE)) 
kJ =  msys.createPrefixedUOM(Prefix.kilo(), msys.getUOM(Unit.JOULE))
qkcal = Quantity(1718, kJ).convert(kcal)
```

One's Body Mass Index (BMI) can be calculated as:
```python
height = Quantity(2, msys.getUOM(Unit.METRE))
mass = Quantity(100, msys.getUOM(Unit.KILOGRAM))
bmi = mass.divide(height.multiply(height))
```

Einstein's famous E = mc^2:
```python
c = msys.getQuantity(Constant.LIGHT_VELOCITY)
m = Quantity(1.0, msys.getUOM(Unit.KILOGRAM))
e = m.multiply(c).multiply(c)
```

```python
# A Tesla Model S battery has a capacity of 100 KwH.  
# When fully charged, how many electrons are in the battery?
c = msys.getQuantity(Constant.LIGHT_VELOCITY)
me = msys.getQuantity(Constant.ELECTRON_MASS)    
kwh = Quantity(100, msys.createPrefixedUOM(Prefix.kilo(), msys.getUOM(Unit.WATT_HOUR)))
electrons = kwh.divide(c).divide(c).divide(me)
```

Ideal Gas Law, PV = nRT.  A cylinder of argon gas contains 50.0 L of Ar at 18.4 atm and 127 °C.  How many moles of argon are in the cylinder?
```python
p = Quantity(18.4, msys.getUOM(Unit.ATMOSPHERE)).convert(msys.getUOM(Unit.PASCAL))
v = Quantity(50, msys.getUOM(Unit.LITRE)).convert(msys.getUOM(Unit.CUBIC_METRE))
t = Quantity(127, msys.getUOM(Unit.CELSIUS)).convert(msys.getUOM(Unit.KELVIN))
n = p.multiply(v).divide(msys.getQuantity(Constant.GAS_CONSTANT).multiply(t))
```

Photon energy using Planck's constant:
```python
# energy of red light photon = Planck's constant times the frequency
frequency = Quantity(400, msys.createPrefixedUOM(Prefix.tera(), msys.getUOM(Unit.HERTZ)))
ev = msys.getQuantity(Constant.PLANCK_CONSTANT).multiply(frequency).convert(msys.getUOM(Unit.ELECTRON_VOLT))

# and wavelength of red light in nanometres (approx 749.48)
wavelength = msys.getQuantity(Constant.LIGHT_VELOCITY).divide(frequency).convert(msys.createPrefixedUOM(Prefix.nano(), msys.getUOM(Unit.METRE)))
```

Newton's second law of motion (F = ma). Weight of 1 kg in lbf:
```python
mkg = Quantity(1, msys.getUOM(Unit.KILOGRAM))
f = mkg.multiply(msys.getQuantity(Constant.GRAVITY)).convert(msys.getUOM(Unit.POUND_FORCE))
```
Units per volume of solution, C = A x (m/V)
```python
mg = msys.createPrefixedUOM(Prefix.milli(), msys.getUOM(Unit.GRAM))

# create the "A" unit of measure
activityUnit = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "activity", "act",
    "activity of material", msys.getUOM(Unit.UNIT), mg)

# calculate concentration
activity = Quantity(1, activityUnit)
grams = Quantity(1000, mg)
mL = msys.createPrefixedUOM(Prefix.milli(), msys.getUOM(Unit.LITRE))
volume = Quantity(1, mL)
concentration = activity.multiply(grams.divide(volume))
qL = Quantity(1, msys.getUOM(Unit.LITRE))
katals = concentration.multiply(qL).convert(msys.getUOM(Unit.KATAL))
```
Black body radiation:

```python
# The Stefan-Boltzmann law states that the power emitted per unit area
# of the surface of a black body is directly proportional to the fourth
# power of its absolute temperature: sigma * T^4
# calculate at 1000 Kelvin
qtemp = Quantity(1000, msys.getUOM(Unit.KELVIN))
qk4 = msys.quantityToPower(qtemp, 4)
intensity = msys.getQuantity(Constant.STEFAN_BOLTZMANN).multiply(qk4)
```

Expansion of the universe:

```python
# Hubble's law, v = H0 x D. Let D = 10 Mpc
d = Quantity(10, msys.createPrefixedUOM(Prefix.mega(), msys.getUOM(Unit.PARSEC)))
h0 = msys.getQuantity(Constant.HUBBLE_CONSTANT)
velocity = h0.multiply(d)
```

Device Characteristic Life

```python
# A device has an activation energy of 0.5 and a characteristic life of
# 2,750 hours at an accelerated temperature of 150 degrees Celsius.
# Calculate the characteristic life at an expected use temperature of
# 85 degrees Celsius.

# Convert the Boltzman constant from J/K to eV/K for the Arrhenius equation
j = Quantity(1, msys.getUOM(Unit.JOULE))
eV = j.convert(msys.getUOM(Unit.ELECTRON_VOLT))
# Boltzmann constant
Kb = msys.getQuantity(Constant.BOLTZMANN_CONSTANT).multiplyByAmount(eV.amount)
# accelerated temperature
Ta = Quantity(150, msys.getUOM(Unit.CELSIUS))
# expected use temperature
Tu = Quantity(85, msys.getUOM(Unit.CELSIUS))
# calculate the acceleration factor
k = msys.getUOM(Unit.KELVIN)
factor1 = Tu.convert(k).invert().subtract(Ta.convert(k).invert())
factor2 = Kb.invert().multiplyByAmount(0.5)
factor3 = factor1.multiply(factor2)
AF = math.exp(factor3.amount)
# calculate longer life at expected use temperature
life85 = Quantity(2750, msys.getUOM(Unit.HOUR))
life150 = life85.multiplyByAmount(AF)
```

## Financial Examples

Value of a stock portfolio:

```python
# John has 100 shares of Alphabet Class A stock. How much is his
# portfolio worth in euros when the last trade was $838.96 and a US
# dollar is worth 0.94 euros?
euro = msys.getUOM(Unit.EURO)
usd = msys.getUOM(Unit.US_DOLLAR)
usd.setConversion(0.94, euro)

googl = msys.createScalarUOM(UnitType.CURRENCY, None, "Alphabet A", "GOOGL",
    "Alphabet (formerly Google) Class A shares")
googl.setConversion(838.96, usd)
portfolio = Quantity(100, googl)
value = portfolio.convert(euro)
            
```

## Medical Examples

```python
# convert Unit to nanokatal
u = msys.getUOM(Unit.UNIT)
katal = msys.getUOM(Unit.KATAL)
q1 = Quantity(1.0, u)
q2 = q1.convert(msys.createPrefixedUOM(Prefix.nano(), katal))

# test result Equivalent
eq = msys.getUOM(Unit.EQUIVALENT)
litre = msys.getUOM(Unit.LITRE)
mEqPerL = msys.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, None, "milliNormal", "mEq/L",
    "solute per litre of solvent ", msys.createPrefixedUOM(Prefix.milli(), eq), litre)
testResult = Quantity(5.0, mEqPerL)

# blood cell count test results
k = msys.createPrefixedUOM(Prefix.kilo(), msys.getOne())
uL = msys.createPrefixedUOM(Prefix.micro(), litre)
kul = msys.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, None, "K/uL", "K/uL",
    "thousands per microlitre", k, uL)
testResult = Quantity(7.0, kul)

fL = msys.createPrefixedUOM(Prefix.femto(), litre)
testResult = Quantity(90, fL)

# TSH test result
uIU = msys.createPrefixedUOM(Prefix.micro(), msys.getUOM(Unit.INTERNATIONAL_UNIT))
mL = msys.createPrefixedUOM(Prefix.milli(), litre)
uiuPerml = msys.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, None, "uIU/mL", "uIU/mL",
    "micro IU per millilitre", uIU, mL)
testResult = Quantity(2.0, uiuPerml)
```

### Caching
A unit of measure once created is registered in two dictionaries, one by its base symbol key and the second one by its enumeration key.  Caching greatly increases performance since the unit of measure is created only once.  Methods are provided to clear the cache of all instances as well as to unregister a particular instance.

The value of a unit of measure conversion is also cached.  This performance optimization eliminates the need to calculate the conversion multiple times if many quantities are being converted at once.  For example, operations upon a vector or matrix of quantities all with the same unit of measure.

## Localization
All externally visible text is defined in two .po files in the /locales/<locale>/LC_MESSAGES folder.  The unit.po file has the name (.name), symbol (.symbol) and description (.desc) for a unit of measure as well as str() method text.  The messages.po file has the text for an exception.  A default US English file for each is included in the project.  The files can be translated to another language by following the locale naming conventions for the .po files folder, or the English version can be edited, e.g. to change "metre" to "meter".  For example, a metre's text is:

```python
# metre
msgid "m.name" 
msgstr "metre"
msgid "m.symbol" 
msgstr "m"
msgid "m.desc" 
msgstr "The length of the path travelled by light in vacuum during a time interval of 1/299792458 of a second."
```

and for an exception:
```python
msgid "must.be.same.as" 
msgstr "The unit of measure {0} of type {1} must be the same as {2} of type {3}."
```

## Project Structure
The PyCaliper library depends on version 3.1+.

The PyCaliper library has the following structure:
 * `/PyCaliper` - docs.zip (HTML API documentation), setup.py
 * `/PyCaliper/uom` - Python library source files, pycaliper.doxygen (Doxygen documentor configuration)
 * `/PyCaliper/uom/locales` - localizable messages.po file to define error messages and localizable units.po file to define the unit's name, symbol and description.
 * `/PyCaliper/test` - unittest source files for the library
 * `/PyCaliper/scripts` - scripts to convert .po to .mo file
