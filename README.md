# PyCaliper
The PyCaliper library project manages units of measure and conversions between them.  PyCaliper is designed to be lightweight and simple to use, yet comprehensive.  It includes a large number of pre-defined units of measure commonly found in science, engineering, technology, finance and the household.  These recognized systems of measurement include the International System of Units (SI), International Customary, United States and British Imperial.  Custom units of measure can also be created in the PyCaliper unified measurement system.  Custom units are specific to a trade or industry such as industrial packaging where units of can, bottle, case and pallet are typical.  Custom units can be added to the unified system for units that are not pre-defined.  The PyCaliper library is also available in Java at https://github.com/point85/Caliper and in C# at https://github.com/point85/PyCaliperSharp.

A PyCaliper measurement system is a collection of units of measure where each pair has a linear relationship, i.e. y = ax + b where 'x' is the abscissa unit to be converted, 'y' (the ordinate) is the converted unit, 'a' is the scaling factor and 'b' is the offset.  In the absence of a defined conversion, a unit will always have a conversion to itself.  A bridge unit conversion is defined to convert between the fundamental SI and International customary units of mass (i.e. kilogram to pound mass), length (i.e. metre to foot) and temperature (i.e. Kelvin to Rankine).  These three bridge conversions permit unit of measure conversions between the two systems.  A custom unit can define any bridge conversion such as a bottle to US fluid ounces or litres.
 
## Concepts

The diagram below illustrates these concepts.
![PyCaliper Diagram](https://github.com/point85/caliper/blob/master/doc/PyCaliperDiagram.png)
 
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

A unit of measure is represented internally as a product of two other power units of measure:

![PyCaliper Diagram](https://github.com/point85/caliper/blob/master/doc/PowerProduct.png)

For a simple scalar UOM (e.g. kilogram), both of the UOMs are null with the exponents defaulted to 0.  For a product UOM (e.g. Newton), the first UOM is the multiplier and the second is the multiplicand with both exponents set to 1.  For a quotient UOM (e.g. kilograms/hour), the first UOM is the dividend and the second is the divisor.  The dividend has an exponent of 1 and the divisor an exponent of -1.  For a power UOM (e.g. square metres), the first UOM is the base and the exponent is the power.  In this case, the second UOM is null with the exponent defaulted to 0.

From the two power products, a unit of measure can then be recursively reduced to a map of base units of measure and corresponding exponents along with a scaling factor.  For example, a Newton reduces to (kg, 1), (m, 1), (s, -2) in the SI system.  Multiplying, dividing and converting a unit of measure is accomplished by merging the two maps (i.e. "cancelling out" units) and then computing the overall scaling factor.  The base symbol is obtained directly from the final map.
 
## Code Examples
The singleton unified MeasurementSystem is obtained by calling:
```python
msys = MeasurementSystem.instance()
```

The units.po file in the /locales/<locale>/LC_MESSAGES folder defines the name, symbol and description for each of the predefined units of measure.  The units.po file is localizable.  It is read by a Singleton instance of the Localizer class.For example, 'metres' can be changed to use the US spelling 'meters' or descriptions can be translated to another language by placing the corresponding .mo file in the appropriate locale folder.

The metre scalar UOM is created by the MeasurementSystem as follows:
```java
uom = msys.createScalarUOM(UnitType.LENGTH, Unit.METRE, Localizer.instance().langStr("m.name"), Localizer.instance().langStr("m.symbol"),
    Localizer.instance().langStr("m.desc"))
``` 

The square metre power UOM is created by the MeasurementSystem as follows: 
```java
uom = msys.createPowerUOM(UnitType.AREA, Unit.SQUARE_METRE, Localizer.instance().langStr("m2.name"),
    Localizer.instance().langStr("m2.symbol"), Localizer.instance().langStr("m2.desc"), msys.getUOM(Unit.METRE), 2)
```

The metre per second quotient UOM is created by the MeasurementSystem as follows: 
```java
uom = msys.createQuotientUOM(UnitType.VELOCITY, Unit.METRE_PER_SEC, Localizer.instance().langStr("mps.name"),
    Localizer.instance().langStr("mps.symbol"), Localizer.instance().langStr("mps.desc"), msys.getUOM(Unit.METRE), msys.getSecond())
```

The Newton product UOM is created by the MeasurementSystem as follows: 
```java
uom = msys.createProductUOM(UnitType.FORCE, unit, Localizer.instance().langStr("newton.name"),
    Localizer.instance().langStr("newton.symbol"), Localizer.instance().langStr("newton.desc"), msys.getUOM(Unit.KILOGRAM),
    msys.getUOM(Unit.METRE_PER_SEC_SQUARED))
```

A millisecond is 1/1000th of a second with a defined prefix and created as:

```java 
msec = msys.createPrefixedUOM(Prefix.milli(), msys.getSecond())
```

For a second example, a US gallon = 231 cubic inches:
```java			
uom = msys.createScalarUOM(UnitType.VOLUME, Unit.US_GALLON,
    Localizer.instance().langStr("us_gallon.name"), Localizer.instance().langStr("us_gallon.symbol"), Localizer.instance().langStr("us_gallon.desc"))
    uom.setConversion(231.0, msys.getUOM(Unit.CUBIC_INCH), 0.0)
```

When creating the foot unit of measure in the unified measurement system, a bridge conversion to metre is defined (1 foot = 0.3048m):
```java
uom = msys.createScalarUOM(UnitType.LENGTH, Unit.FOOT, Localizer.instance().langStr("foot.name"),
    Localizer.instance().langStr("foot.symbol"), Localizer.instance().langStr("foot.desc"))
    
    # bridge to SI
    uom.setBridgeConversion(0.3048, self.getUOM(Unit.METRE), 0.0)
```

Custom units of measure (with no pre-defined Unit) and conversions can also be created:
```java
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
```java
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
```java
q1 = Quantity(50.0, cm)
q2 = Quantity(50.0, cm)
        
# q3 = 2500 cm^2
q3 = q1.multiply(q2)
        
# q4 = 50 cm
q4 = q3.divide(q1)
```

and inverted:
```java
mps = msys.getUOM(Unit.METRE_PER_SEC) 
q1 = Quantity(10.0, mps)
        
# q2 = 0.1 sec/m
q2 = q1.invert()
```

To make working with linearly scaled units of measure (with no offset) easier, the MeasurementSystem's createPrefixedUOMUOM() method that uses a Prefix can be used.  This method accepts a Prefix enum and the unit of measure that it is scaled against.  The resulting unit of measure has a name concatented with the Prefix's name and target unit name.  The symbol is formed similarly.  For example, a centilitre (cL) is created from the pre-defined litre by:
```java
litre = msys.getUOM(Unit.LITRE)
cL = msys.createPrefixedUOM(Prefix.centi(), litre)
```
and, a megabyte (MB = 2^20 bytes) is created by:
```java
mB = msys.createPrefixedUOM(Prefix.mebi(), msys.getUOM(Unit.BYTE))
```

*Implicit Conversions*

A quantity can be converted to another unit of measure without requiring the target UOM to first be created.  If the quantity has a product or quotient UOM, use the convertToPowerProduct() method.  For example:

```java
# convert 1 newton-metre to pound force-inches
nmQ = Quantity(1.0, msys.getUOM(Unit.NEWTON_METRE))
lbfinQ = nmQ.convertToPowerProduct(msys.getUOM(Unit.POUND_FORCE), msys.getUOM(Unit.INCH))
```

If the quantity has power UOM, use the convertToPower() method.  For example:

```java
# convert 1 square metre to square inches
m2Q = Quantity(1.0, msys.getUOM(Unit.SQUARE_METRE))
in2Q = m2Q.convertToPower(msys.getUOM(Unit.INCH))
```

Other UOMs can be converted using the convert() method.

*Classification*

During arithmetic operations, the final type of the unit may not be known.  In this case, invoking the classify() method will attempt to find a matching unit type.  For example, the calculated unit of measure below has a type of UnitType.ELECTRIC_CAPACITANCE:

```java
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

```java
mass = Quantity(1035, msys.getUOM(Unit.KILOGRAM))
volume = Quantity(1000, msys.getUOM(Unit.LITRE))
density = mass.divide(volume).classify()
```

## Physical Unit Examples

Water boils at 100 degrees Celcius.  What is this temperature in Fahrenheit?
```java
qC = Quantity(100.0, msys.getUOM(Unit.CELSIUS))
qF = qC.convert(msys.getUOM(Unit.FAHRENHEIT))
```

A nutrition label states the energy content is 1718 KJ.  What is this amount in kilo-calories?
```java
kcal = msys.createPrefixedUOM(Prefix.kilo(), msys.getUOM(Unit.CALORIE)) 
kJ =  msys.createPrefixedUOM(Prefix.kilo(), msys.getUOM(Unit.JOULE))
qkcal = Quantity(1718, kJ).convert(kcal)
```

One's Body Mass Index (BMI) can be calculated as:
```java
height = Quantity(2, msys.getUOM(Unit.METRE))
mass = Quantity(100, msys.getUOM(Unit.KILOGRAM))
bmi = mass.divide(height.multiply(height))
```

Einstein's famous E = mc^2:
```java
c = msys.getQuantity(Constant.LIGHT_VELOCITY)
m = Quantity(1.0, msys.getUOM(Unit.KILOGRAM))
e = m.multiply(c).multiply(c)
```

```java
// A Tesla Model S battery has a capacity of 100 KwH.  
// When fully charged, how many electrons are in the battery?
c = msys.getQuantity(Constant.LIGHT_VELOCITY)
me = msys.getQuantity(Constant.ELECTRON_MASS)    
kwh = Quantity(100, msys.createPrefixedUOM(Prefix.kilo(), msys.getUOM(Unit.WATT_HOUR)))
electrons = kwh.divide(c).divide(c).divide(me)
```

Ideal Gas Law, PV = nRT.  A cylinder of argon gas contains 50.0 L of Ar at 18.4 atm and 127 °C.  How many moles of argon are in the cylinder?
```java
p = Quantity(18.4, msys.getUOM(Unit.ATMOSPHERE)).convert(msys.getUOM(Unit.PASCAL))
v = Quantity(50, msys.getUOM(Unit.LITRE)).convert(msys.getUOM(Unit.CUBIC_METRE))
t = Quantity(127, msys.getUOM(Unit.CELSIUS)).convert(msys.getUOM(Unit.KELVIN))
n = p.multiply(v).divide(msys.getQuantity(Constant.GAS_CONSTANT).multiply(t))
```

Photon energy using Planck's constant:
```java
# energy of red light photon = Planck's constant times the frequency
frequency = Quantity(400, msys.createPrefixedUOM(Prefix.tera(), msys.getUOM(Unit.HERTZ)))
ev = msys.getQuantity(Constant.PLANCK_CONSTANT).multiply(frequency).convert(msys.getUOM(Unit.ELECTRON_VOLT))

# and wavelength of red light in nanometres (approx 749.48)
wavelength = msys.getQuantity(Constant.LIGHT_VELOCITY).divide(frequency).convert(msys.createPrefixedUOM(Prefix.nano(), msys.getUOM(Unit.METRE)))
```

Newton's second law of motion (F = ma). Weight of 1 kg in lbf:
```java
mkg = Quantity(1, msys.getUOM(Unit.KILOGRAM))
f = mkg.multiply(msys.getQuantity(Constant.GRAVITY)).convert(msys.getUOM(Unit.POUND_FORCE))
```
Units per volume of solution, C = A x (m/V)
```java
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

```java
# The Stefan-Boltzmann law states that the power emitted per unit area
# of the surface of a black body is directly proportional to the fourth
# power of its absolute temperature: sigma * T^4
# calculate at 1000 Kelvin
qtemp = Quantity(1000, msys.getUOM(Unit.KELVIN))
qk4 = msys.quantityToPower(qtemp, 4)
intensity = msys.getQuantity(Constant.STEFAN_BOLTZMANN).multiply(qk4)
```

Expansion of the universe:

```java
# Hubble's law, v = H0 x D. Let D = 10 Mpc
d = Quantity(10, msys.createPrefixedUOM(Prefix.mega(), msys.getUOM(Unit.PARSEC)))
h0 = msys.getQuantity(Constant.HUBBLE_CONSTANT)
velocity = h0.multiply(d)
```

Device Characteristic Life

```java
// A device has an activation energy of 0.5 and a characteristic life of
// 2,750 hours at an accelerated temperature of 150 degrees Celsius.
// Calculate the characteristic life at an expected use temperature of
// 85 degrees Celsius.

// Convert the Boltzman constant from J/K to eV/K for the Arrhenius equation
Quantity j = new Quantity(1d, Unit.JOULE)
Quantity eV = j.convert(Unit.ELECTRON_VOLT)
// Boltzmann constant
Quantity Kb = sys.getQuantity(Constant.BOLTZMANN_CONSTANT).multiply(eV.getAmount())
// accelerated temperature
Quantity Ta = new Quantity(150d, Unit.CELSIUS)
// expected use temperature
Quantity Tu = new Quantity(85d, Unit.CELSIUS)
// calculate the acceleration factor
Quantity factor1 = Tu.convert(Unit.KELVIN).invert().subtract(Ta.convert(Unit.KELVIN).invert())
Quantity factor2 = Kb.invert().multiply(0.5)
Quantity factor3 = factor1.multiply(factor2)
double AF = Math.exp(factor3.getAmount())
// calculate longer life at expected use temperature
Quantity life85 = new Quantity(2750d, Unit.HOUR)
Quantity life150 = life85.multiply(AF)
```

## Financial Examples

Value of a stock portfolio:

```java
// John has 100 shares of Alphabet Class A stock. How much is his
// portfolio worth in euros when the last trade was $838.96 and a US
// dollar is worth 0.94 euros?
euro = sys.getUOM(Unit.EURO)
usd = sys.getUOM(Unit.US_DOLLAR)
usd.setConversion(0.94, euro)

googl = sys.createScalarUOM(UnitType.CURRENCY, "Alphabet A", "GOOGL",
	"Alphabet (formerly Google) Class A shares")
googl.setConversion(838.96, usd)
Quantity portfolio = new Quantity(100, googl)
Quantity value = portfolio.convert(euro)
```

## Medical Examples

```java
// convert Unit to nanokatal
u = sys.getUOM(Unit.UNIT)
katal = sys.getUOM(Unit.KATAL)
Quantity q1 = new Quantity(1.0, u)
Quantity q2 = q1.convert(sys.getUOM(Prefix.NANO, katal))

// test result Equivalent
eq = sys.getUOM(Unit.EQUIVALENT)
litre = sys.getUOM(Unit.LITRE)
mEqPerL = sys.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, "milliNormal", "mEq/L",
	"solute per litre of solvent ", sys.getUOM(Prefix.MILLI, eq), litre)
Quantity testResult = new Quantity(5.0, mEqPerL)

// blood cell count test results
k = sys.getUOM(Prefix.KILO, sys.getOne())
uL = sys.getUOM(Prefix.MICRO, Unit.LITRE)
kul = sys.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, "K/uL", "K/uL",
	"thousands per microlitre", k, uL)
testResult = new Quantity(7.0, kul)

fL = sys.getUOM(Prefix.FEMTO, Unit.LITRE)
testResult = new Quantity(90d, fL)

// TSH test result
uIU = sys.getUOM(Prefix.MICRO, Unit.INTERNATIONAL_UNIT)
mL = sys.getUOM(Prefix.MILLI, Unit.LITRE)
uiuPerml = sys.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, "uIU/mL", "uIU/mL",
	"micro IU per millilitre", uIU, mL)
testResult = new Quantity(2.0, uiuPerml)
```

### Caching
A unit of measure once created is registered in two hashmaps, one by its base symbol key and the second one by its enumeration key.  Caching greatly increases performance since the unit of measure is created only once.  Methods are provided to clear the cache of all instances as well as to unregister a particular instance.

The double value of a unit of measure conversion is also cached.  This performance optimization eliminates the need to calculate the conversion multiple times if many quantities are being converted at once for example, operations upon a vector or matrix of quantities all with the same unit of measure.

## Localization
All externally visible text is defined in two resource bundle .properties files.  The Unit.properties file has the name (.name), symbol (.symbol) and description (.desc) for a unit of measure as well as toString() method text.  The Message.properties file has the text for an exception.  A default English file for each is included in the project.  The files can be translated to another language by following the Java locale naming conventions for the properties file, or the English version can be edited, e.g. to change "metre" to "meter".  For example, a metre's text is:

```java
# metre
m.name = metre
m.symbol = m
m.desc = The length of the path travelled by light in vacuum during a time interval of 1/299792458 of a second.
```

and for an exception:
```java
already.created = The unit of measure with symbol {0} has already been created by {1}.  Did you intend to scale this unit with a linear conversion?
```

## Unit of Measure Application
An example Unit of Measure converter and editor desktop application has been built to demonstrate fundamental capabilities of the library.  The user interface is implemented in JavaFX 8 and database persistency is provided by JPA (Java Persistence API) with FXML descriptors.  EclipseLink is the JPA implementation for a Microsoft SQL Server database.

The editor allows new units of measure to be created and saved to the database as well as updated and deleted.  All of the units of measure pre-defined in the library are available for use in the editor or in the converter. 

The screen capture below shows the converter:
![PyCaliper Diagram](https://github.com/point85/caliper/blob/master/doc/UOM_Converter.png)

The "Editor ..." button launches the editor (see below).  To convert a unit of measure follow these steps:
*  Select the unit type in the drop-down, e.g. LENGTH.  
*  Enter the amount to convert from, e.g. 1
*  Select the from prefix if desired.  For example, "kilo" is 1000 of the units.
*  Select the from unit of measure, e.g. "m (metre)" in the drop-down.
*  Select the to prefix if desired.  
*  Select the to unit of measure, e.g. "mi (mile)" in the drop-down.
*  Click the "Convert" button.  The converted amount will be displayed below the from amount, e.g. 0.621371192.

The screen capture below shows the unit of measure editor:
![PyCaliper Diagram](https://github.com/point85/caliper/blob/master/doc/UOM_Editor.png) 

To create a unit of measure, click the "New" button and follow these steps:
*  Enter a name, symbol, category (or choose one already defined) and description.
*  Choose the type from the drop-down.  For custom units, choose "UNCLASSIFIED".  Only units of the same type can be converted.
*  If the unit of measure is related to another unit of measure via a conversion, enter the scaling factor (a), abscissa (x) and offset (b).  A prefix (e.g. kilo) may be chosen for the scaling factor.  The conversion will default to the unit of measure itmsys.
*  For a simple scalar unit, no additional properties are required.
*  For a product or quotient unit of measure, the multiplier/multiplicand or dividend/divisor properties must be entered.  First select the respective unit type (e.g. VOLUME) then the unit of measure.  Click the respective radio button to indicate whether this is product or quotient.
*  For a power unit, the base unit of measure and exponent must be entered.  First select the unit type, then the base unit of measure.  Enter the exponent.
*  Click the "Save" button.  The new unit of measure will appear in the tree view on the left under its category.


To edit a unit of measure, select it in the tree view.  It's properties will be displayed on the right.  Change properties as required, then click the "Save" button.

To refresh the state of the unit that is selected in the tree view from the database, click the "Refresh" button.

To delete a unit of measure, select it in the tree view then click the "Delete" button.


## Project Structure
The PyCaliper library depends on Java 6+.  The unit tests depend on JUnit (http://junit.org/junit4/), Hamcrest (http://hamcrest.org/), Gson (https://github.com/google/gson) and HTTP Request (https://github.com/kevinsawicki/http-request).  The example application depends on Java 8+ and a JPA implementation (e.g. EclipseLink http://www.eclipse.org/eclipselink/#jpa).

The PyCaliper library and application, when built with Gradle, has the following structure:
 * `/build/docs/javadoc` - javadoc files for the library
 * `/build/libs` - compiled caliper.jar library
 * `/doc` - documentation
 * `/src/main/java` - java library source files
 * `/src/main/resources` - localizable Message.properties file to define error messages and localizable Unit.properties file to define the unit's name, symbol and description.
 * `/src/test/java` - JUnit test java source files for the library
 * `/src/ui/java` - java source files for JPA persistency and JavaFX 8 user interface for the application
 * `/src/ui/resources` - images and XML files for for JPA persistency
 * `/database` - SQL script files for table and index generation

## JSR 363
JSR 363 "proposes to establish safe and useful methods for modeling physical quantities" (https://java.net/downloads/unitsofmeasurement/JSR363Specification_EDR.pdf).  PyCaliper shares many of the underlying aspects of JSR 363.  PyCaliper however does not use Java generics, and there is only one system of units.  PyCaliper performs math using double amounts whereas JSR 363 uses Numbers.

The tables below compare the JSR 363 specification in the first column to Point85 in the second column.

![PyCaliper Diagram](https://github.com/point85/caliper/blob/master/doc/jsr363_type.png)

![PyCaliper Diagram](https://github.com/point85/caliper/blob/master/doc/jsr363_uom.png)

![PyCaliper Diagram](https://github.com/point85/caliper/blob/master/doc/jsr363_quantity.png)

![PyCaliper Diagram](https://github.com/point85/caliper/blob/master/doc/jsr363_rest.png)




