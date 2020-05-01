# agh.sprintf.js

C, POSIX compatible sprintf written in JavaScript.

License: MIT License

See [日本語の説明](https://github.com/akinomyoga/agh.sprintf.js/blob/master/README.ja_JP.md) for the Japanese README texts.

**HTML**

```html
<script type="text/javascript" charset="utf-8" src="agh.sprintf.js"></script>
<script type="text/javascript">
var result1 = sprintf("pi = %-*.*g /* this is an example */", 30, 20, Math.PI);
var result2 = vsprintf("pi = %-*.*g /* this is an example */", [30, 20, Math.PI]);
</script>
```

**Node**

```sh
$ npm install agh.sprintf
```

```javascript
const agh = require('agh.sprintf');
console.log(agh.sprintf("pi = %-*.*g /* this is an example */", 30, 20, Math.PI));
console.log(agh.vsprintf("pi = %-*.*g /* this is an example */", [30, 20, Math.PI]));
```

**Node (without npm)**

```sh
$ git clone https://github.com/akinomyoga/agh.sprintf.js
$ cd agh.sprintf.js
```

```javascript
const agh = require('./agh.sprintf.js');
console.log(agh.sprintf("pi = %-*.*g /* this is an example */", 30, 20, Math.PI));
console.log(agh.vsprintf("pi = %-*.*g /* this is an example */", [30, 20, Math.PI]));
```

## 1 Format specifiers

The first argument of sprintf is a format string which may include the following form of format specifiers:

`'%'` *\<pos>***?** *\<flags>***?** *\<width>***?** *\<precision>***?** *\<type>***?** *\<conv>*

 - The conversion specifier *\<conv>* specifies an output format.
 - The width specifier *\<width>* specifies a minimal number of characters output.
 - The precision specifier *\<precision>* specifies a *precision* of the output.
 - The flags *\<flags>* control the detailed behavior of padding, prefix, etc.
 - The position parameter *\<pos>* specifies an argument by its index.
 - The size specifier *\<type>* determines the data type of the argument.

### 1.1 Conversion specifier *\<conv>*

A conversion specifier determines the interpretation of an argument and the format of the output.

|Specifier|Standard|Description|
|:--|:--|:--|
|`'d', 'i'`|ANSI C|decimal signed number
|`'o'`     |ANSI C|octal unsigned number
|`'u'`     |ANSI C|decimal unsigned number
|`'x', 'X'`|ANSI C|hexadecimal unsigned number. lower/upper case corresponds to, e.g., 0xa/0XA.
|`'f', 'F'`|ANSI C|floating point numbers. lower/upper case corresponds to, e.g., inf/INF.
|`'e', 'E'`|ANSI C|floating point numbers by the scientific representation. lower/upper case corresponds to, e.g., 1e+5/1E+5.
|`'g', 'G'`|ANSI C|floating point numbers with the specified precision.
|`'a', 'A'`|C99   |floating point numbers in hexadecimal.
|`'c'`     |ANSI C|character
|`'C'`     |XSI   |character (same as `'c'` in this implementation. Originally, the argument is interpreted as `wchar_t`.)
|`'s'`     |ANSI C|string
|`'S'`     |XSI   |string (same as `'s'` in this implementation. Originally, the argument is interpreted as `wchar_t`)
|`'p'`     |ANSI C|pointer (same as `%#x` in this implementation)
|`'n'`     |ANSI C|stores to `value[0]` the number of the characters output until this point
|`'%'`     |ANSI C|output "%"

```javascript
// Examples
agh.sprintf("%d", 12345); // "12345"
agh.sprintf("%o", 12345); // "30071"
agh.sprintf("%u", -12345); // "4294954951"
agh.sprintf("%x", 54321); // "d431"
agh.sprintf("%X", 54321); // "D431"
agh.sprintf("%f", Math.PI); // "3.141593"
agh.sprintf("%e", Math.PI); // "3.141593e+000"
agh.sprintf("%g", Math.PI); // "3.14159"
agh.sprintf("%a", Math.PI); // "0x1.921fb54442d18p+001"
agh.sprintf("%f, %F", Number.POSITIVE_INFINITY, Number.POSITIVE_INFINITY); // "inf, INF"
agh.sprintf("%c, %C", 12354, 12354); // "あ, あ"
agh.sprintf("%s, %S", 12354, 12354); // "12354, 12354"
agh.sprintf("%d", 12345); // "12345"
agh.sprintf("%p", 12345); // "0x3039"
agh.sprintf("%d%n", 12345, a = []); // "12345", a == [5]
agh.sprintf("%%"); // "%"
```

### 1.2 Width specifier *\<width>*

The width specifier has the following form:

*\<width>* **:=** `/\d+/` **|** `'*'` **|** `'*'` `/\d+/` `'$'`

| Specifier | Standard | Description |
|:--|:--|:--|
|`/\d+/`        |ANSI C|The minimal width is directly specified.|
|`'*'`          |ANSI C|The next argument is consumed for the minimal width.|
|`'*'` `/\d+/` `'$'`|POSIX|The argument specified with the index is used for the minimal width.|

```javascript
// Examples
agh.sprintf("[%1d]", 12345); // "[12345]"
agh.sprintf("[%8d]", 12345); // "[   12345]" 
agh.sprintf("[%*d]", 6, 12345); // "[ 12345]"
agh.sprintf("[%*2$d]", 12345, 7); // "[  12345]"
```

### 1.3 Precision specifier *\<precision>*

The precision specifier has the following form:

*\<precision>* **:=** `'.'` `/\d+/` **|** `'.*'` **|** `'.*'` `/\d+/` `'$'`

|Specifier|Standard|Description|
|:--|:--|:--|
|`'.'` `/\d+/`       |ANSI C|The precision is directly specified.
|`'.*'`              |ANSI C|The next argument is consumed for the precision.
|`'.*'` `/\d+/` `'$'`|POSIX |The argument specified with the index is used for the precision.

In the case of the integer converesions (*\<conv>* = d, i, u, o, x, and X), the precision specifies the minimal number of digits with redundant higher digits being filled by zeroes. For example, 1 will be "0001" with the precision of 4. With the precision, the flag "`0`" will be ignored.

In the case that *\<conv>* = f, F, e, E, a, and A, the precision specifies the number of digits after the decimal point. In the case that *\<conv>* = g and G, the precision is the number of the significant digits. The default value of the precision for *\<conv>* = f, F, e, E, g, and G is 6. The default value for *\<conv>* = a and A is 13 which is the hexadecimal precision of the double precision floating point numbers.

For the strings *\<conv>* = s and S, the precision specifies the maximal number of characters to output. Extra characters will be discarded.

```javascript
// Examples
agh.sprintf("%.1d", 12345); // "12345"
agh.sprintf("%.8d", 12345); // "00012345" 
agh.sprintf("%.*d", 6, 12345); // "012345"
agh.sprintf("%.*2$d", 12345, 7); // "0012345"
agh.sprintf("%.1f", Math.PI); // "3.1"
agh.sprintf("%.10f", Math.PI); // "3.1415926536"
agh.sprintf("%.50f", Math.PI); // "3.14159265358979311599796346854418516159057617187500"
agh.sprintf("%.1g", Math.PI); // "3"
agh.sprintf("%.10g", Math.PI); // "3.141592654"
agh.sprintf("%.1s", "12345"); // "1"
agh.sprintf("%.10s", "12345"); // "12345"
```

### 1.4 Flags *\<flags>*

The flag specifier has the following form:

*\<flags>* **:= (** `/[-+ 0#']/` **|** `/\=./` **) +**

| Flag | Standard | Description |
|:--|:--|:--|
|`'-'`|ANSI C|The left justification instead of the default of the right justification|
|`'+'`|ANSI C|The plus sign for positive numbers|
|`'#'`|ANSI C|For the integer conversions, the prefix representing its base will be added if the value is not zero. The prefixes are "0", "0x", and "0X" for *\<conv>* = o, x, and X, respectively.<br>For the floating point numbers, this flag prevent to omit the decimal point even if the value is an integer. In addition, trailing zeroes will not be omitted for *\<conv>* = g and G.|
|`' '`|ANSI C|A space is output at the sign position for positive numbers. This space is not omitted even if the output width excesses the specified *\<width>*.|
|`'0'`|ANSI C|Use "`0`" instead of "` `" for the left padding. Note that, unlike the spaces, `0`s are inserted after the sign and the prefixes.|
|`"'"`|SUSv2|The grouping characaters, i.e. commas at every three digits, are inserted in the integral part for *\<conv>* = d, i, f, F, g, and G. Note that, the grouping characters are not inserted for the zero padding specified by the flag "`0`".|

```javascript
// Examples
agh.sprintf("[%3d][%-3d]", 1, 1); // "[  1][1  ]"
agh.sprintf("%d, %+d", 1, 1); // "1, +1"
agh.sprintf("%o, %#o, %#o", 1, 1, 0); // "1, 01, 0"
agh.sprintf("%x, %#x, %#x", 1, 1, 0); // "1, 0x1, 0"
agh.sprintf("[%d][% d]", 1, 1); // "[1][ 1]"
agh.sprintf("[%4d][%04d]", 1, 1); // "[   1][0001]"
agh.sprintf("%d, %'d", 1234567, 1234567); // "1234567, 1,234,567"
```

### 1.5 Positional parameter *\<pos>*

The positional parameter has the following form:

*\<pos>* **:=** `/\d+\$/`

It selects an argument to output by its index. The argument just after the format string corresponds to the index 1.

```javascript
// Example
agh.sprintf("%3$d %2$d %1$d %2$d %3$d", 111, 222, 333); // "333 222 111 222 333"
```

### 1.6 Size specifier *\<type>*

The size specifier determines the exact type of the argument, e.g. the binary representation of the integers and the floating point numbers. The size specifier has a different meaning for each conversion:

For the integers (*\<conv>* = d, i, o, u, x, and X),

|Size   |Standard (typical meaning)|Implementation|
|:------|:-----------------------|:-----|
|(default)|ANSI C (int)          |double|
|`'hh'` |C99  (char)             |  8bit|
|`'h'`  |ANSI C (short)          | 16bit|
|`'l'`  |ANSI C (long)           | 32bit|
|`'ll'` |C99  (long long)        | 32bit|
|`'t'`  |C99  (ptrdiff_t)        | 32bit|
|`'z'`  |C99  (size_t)           | 32bit|
|`'I'`  |MSVC (ptrdiff_t, size_t)| 32bit|
|`'I32'`|MSVC (32bit)            | 32bit|
|`'q'`  |BSD  (64bit)            | 64bit|
|`'I64'`|MSVC (64bit)            | 64bit|
|`'j'`  |C99  (intmax_t)         |double|

 - If nothing is specified, the integer can be `double` value since the internal representation of the integers is `double` in JavaScript.
 - The bit width for ptrdiff_t, size_t, long, and long long is 32 bits because the JavaScript integer does not have the precision of 64 bits.
 - The explicit 64 bit specifiers, `q` and `I64`, may not result in correct output.

```javascript
// Examples
agh.sprintf("%x", 123456789); // "75bcd15"
agh.sprintf("%hx", 123456789); // "cd15"
agh.sprintf("%hhx", 123456789); // "15"
```

For the floating point numbers (*\<conv>* = f, F, e, E, g, G, a, and A),

|Size   |Standard                |Description|
|:------|:-----------------------|:-----|
|(default) |ANSI C (double)      |double|
|`'hh'` |*Original*              | float|
|`'h'`  |*Original*              | float|
|`'l'`  |C99  (double)           |double|
|`'ll'` |*Original*              |double|
|`'L'`  |ANSI C (long double)    |double|
|`'w'`  |*Original*              |double|

 - The type `double` is used instead of `long double` since JavaScript does not have the type.
 - The sizes `hh`, `h`, `l`, `ll`, and `w` are used for other conversions in standards.

```javascript
// Examples
agh.sprintf("%.15g", Math.PI);  // "3.14159265358979"
agh.sprintf("%.15hg", Math.PI); // "3.14159250259399"
```

For characters and strings (*\<conv>* = c, C, s, and S), 

|Size  |Standard       |Description   |
|:-----|:--------------|:------|
|(default)|ANSI C      |unicode|
|`'hh'`|*Original*     |  ascii|
|`'h'` |MSVC (char)    |  ascii|
|`'l'` |C99  (wint_t)  |unicode|
|`'w'` |MSVC (wchar_t) |unicode|

```javascript
// Examples
agh.sprintf("%c", 12354); // "あ"
agh.sprintf("%hc", 12354); // "B"
```

## 2 (ToDo)

README: Comparisions with other implementations?

sprintf.js: Padding character specifier `=?`, Named arguments, filters
