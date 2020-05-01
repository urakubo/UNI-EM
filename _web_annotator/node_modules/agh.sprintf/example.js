const agh = require("agh.sprintf");

// integers

console.log(agh.sprintf("%d, %d", 12345, -12345)); // "12345, -12345"
console.log(agh.sprintf("%o, %o", 12345, -12345)); // "30071, 37777747707"
console.log(agh.sprintf("%u, %u", 12345, -12345)); // "12345, 4294954951"
console.log(agh.sprintf("%x, %X", 54321, 54321));  // "d431, D431"          

// floating-point numbers

const pi = Math.PI, infty = Number.POSITIVE_INFINITY;
console.log(agh.sprintf("%f, %e, %g, %a", pi, pi, pi, pi)); // "3.141593, 3.141593e+000, 3.14159, 0x1.921fb54442d18p+001"
console.log(agh.sprintf("%f, %F", infty, infty)); // "inf, INF"

// characters/strings

console.log(agh.sprintf("%c, %s", 12354, 12354)); // "あ, 12354"

// misc conversions

const arr = [];
console.log(agh.sprintf("%p, %%, %n", 12345, arr)); // "0x3039, %, "
console.log(arr[0]); // 11

// width

console.log(agh.sprintf("[%8d][%*d][%*5$d]", 12345, 6, 12345, 12345, 7)); // "[   12345][ 12345][  12345]"

// precision

console.log(agh.sprintf("%.8d, %.*d, %.*5$d", 12345, 6, 12345, 12345, 7)); // "00012345, 012345, 0012345"
console.log(agh.sprintf("%.1g, %.10g", pi, pi)); // "3, 3.141592654"

// flags

console.log(agh.sprintf("%3d:%-3d:%03d", 1, 1, 1)); // "  1:1  :001"
console.log(agh.sprintf("%d:%+d:% d", 1, 1, 1)); // "1:+1: 1"
console.log(agh.sprintf("%#o:%#x:%#o:%#x", 1, 1, 0, 0)); // "01:0x1:0:0"
console.log(agh.sprintf("%d, %'d", 1234567, 1234567)); // "1234567, 1,234,567"

// positional parameters

console.log(agh.sprintf("%3$d %2$d %1$d %2$d %3$d", 111, 222, 333)); // "333 222 111 222 333"
