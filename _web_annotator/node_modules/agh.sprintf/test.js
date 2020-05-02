const agh = require('.');

function assert(result) {
  if (!result) throw new Error("assertion failed.");
}
function assert_eq(value, expected) {
  if (value != expected)
    throw new Error("assertion failed: value = " + value + ", expected = " + expected);
}

const pi = Math.PI, infinity = Number.POSITIVE_INFINITY;

assert_eq(agh.sprintf("%d", 12345), "12345");
assert_eq(agh.sprintf("%o", 12345), "30071");
assert_eq(agh.sprintf("%u", -12345), "4294954951");
assert_eq(agh.sprintf("%x", 54321), "d431");
assert_eq(agh.sprintf("%X", 54321), "D431");
assert_eq(agh.sprintf("%f", pi), "3.141593");
assert_eq(agh.sprintf("%e", pi), "3.141593e+000");
assert_eq(agh.sprintf("%g", pi), "3.14159");
assert_eq(agh.sprintf("%a", pi), "0x1.921fb54442d18p+001");
assert_eq(agh.sprintf("%f, %F", infinity, infinity), "inf, INF");
assert_eq(agh.sprintf("%c, %C", 12354, 12354), "あ, あ");
assert_eq(agh.sprintf("%s, %S", 12354, 12354), "12354, 12354");
assert_eq(agh.sprintf("%d", 12345), "12345");
assert_eq(agh.sprintf("%p", 12345), "0x3039");
assert_eq(agh.sprintf("%%"), "%");

var a = [];
assert_eq(agh.sprintf("%d%n", 12345, a), "12345");
assert_eq(a[0], 5);

assert_eq(agh.sprintf("[%1d]", 12345), "[12345]");
assert_eq(agh.sprintf("[%8d]", 12345), "[   12345]" );
assert_eq(agh.sprintf("[%*d]", 6, 12345), "[ 12345]");
assert_eq(agh.sprintf("[%*2$d]", 12345, 7), "[  12345]");

assert_eq(agh.sprintf("%.1d", 12345), "12345");
assert_eq(agh.sprintf("%.8d", 12345), "00012345" );
assert_eq(agh.sprintf("%.*d", 6, 12345), "012345");
assert_eq(agh.sprintf("%.*2$d", 12345, 7), "0012345");
assert_eq(agh.sprintf("%.1f", pi), "3.1");
assert_eq(agh.sprintf("%.10f", pi), "3.1415926536");
assert_eq(agh.sprintf("%.50f", pi), "3.14159265358979311599796346854418516159057617187500");
assert_eq(agh.sprintf("%.1g", pi), "3");
assert_eq(agh.sprintf("%.10g", pi), "3.141592654");
assert_eq(agh.sprintf("%.1s", "12345"), "1");
assert_eq(agh.sprintf("%.10s", "12345"), "12345");

assert_eq(agh.sprintf("[%3d][%-3d]", 1, 1), "[  1][1  ]");
assert_eq(agh.sprintf("%d, %+d", 1, 1), "1, +1");
assert_eq(agh.sprintf("%o, %#o, %#o", 1, 1, 0), "1, 01, 0");
assert_eq(agh.sprintf("%x, %#x, %#x", 1, 1, 0), "1, 0x1, 0");
assert_eq(agh.sprintf("[%d][% d]", 1, 1), "[1][ 1]");
assert_eq(agh.sprintf("[%4d][%04d]", 1, 1), "[   1][0001]");
assert_eq(agh.sprintf("%d, %'d", 1234567, 1234567), "1234567, 1,234,567");

assert_eq(agh.sprintf("%3$d %2$d %1$d %2$d %3$d", 111, 222, 333), "333 222 111 222 333");

assert_eq(agh.sprintf("%x", 123456789), "75bcd15");
assert_eq(agh.sprintf("%hx", 123456789), "cd15");
assert_eq(agh.sprintf("%hhx", 123456789), "15");

assert_eq(agh.sprintf("%.15g", pi), "3.14159265358979");
assert_eq(agh.sprintf("%.15hg", pi), "3.14159250259399");

assert_eq(agh.sprintf("%c", 12354), "あ");
assert_eq(agh.sprintf("%hc", 12354), "B");

assert_eq(agh.sprintf("%2$d行目のコマンド %1$sは不正です", "hoge", 20), "20行目のコマンド hogeは不正です");
assert_eq(agh.sprintf("%d %o %x\n", 1234, 1234, 1234), "1234 2322 4d2\n");
assert_eq(agh.sprintf("%s %c\n", "abc", 'x'.charCodeAt(0)), "abc x\n");
assert_eq(agh.sprintf("%*d", 5, 10), "   10");
assert_eq(agh.sprintf("%.*s", 3, "abcdef"), "abc");
assert_eq(agh.sprintf("%2d %02d", 3, 3), " 3 03");
assert_eq(agh.sprintf("%1$d:%2$.*3$d:%4$.*3$d\n", 15, 35, 3, 45), "15:035:045\n");

assert_eq(agh.sprintf("%%d: [%+10d][%+ 10d][% +10d][%d]", 10, 10, 10, 1e10), "%d: [       +10][       +10][       +10][10000000000]");
assert_eq(agh.sprintf("%%u: [%u][%u][%+u][% u][%-u][%+10u][%-10u]", -1, 10, 10, 10, 10, 10, 10), "%u: [4294967295][10][10][10][10][        10][10        ]");
assert_eq(agh.sprintf("%%x,%%u: %x %o", -1, -1), "%x,%u: ffffffff 37777777777");
assert_eq(agh.sprintf("%%a: %a %a %a %a %a %a %a %a %a", 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
          "%a: 0x1.999999999999ap-004 0x1.999999999999ap-003 0x1.3333333333333p-002 0x1.999999999999ap-002 0x1p-001"
          + " 0x1.3333333333333p-001 0x1.6666666666666p-001 0x1.999999999999ap-001 0x1.ccccccccccccdp-001");
assert_eq(agh.sprintf("%%A: %A %.3A %#.3A", 1e10, 1e10, 1e10), "%A: 0X1.2A05F2P+033 0X1.2AP+033 0X1.2AP+033");
assert_eq(agh.sprintf("%%A: %A %A %A %A", 4096, 2048, 1024, 512), "%A: 0X1P+012 0X1P+011 0X1P+010 0X1P+009");

assert_eq(agh.sprintf("%%e: %#.3e %#.3e %#.3e", 1e1000, 1e100, 1e10), "%e: inf 1.000e+100 1.000e+010");
assert_eq(agh.sprintf("%%e: %#.3e %#.6e %#.10e %#.20e\n", 1.234, 1.234, 1.234, 1.234),
          "%e: 1.234e+000 1.234000e+000 1.2340000000e+000 1.23399999999999998579e+000\n");
assert_eq(agh.sprintf("%%e: %#.1e %#.5e %#.10e %#.100e", 9.999, 9.999, 9.999, 9.999),
          "%e: 1.0e+001 9.99900e+000 9.9990000000e+000"
          + " 9.9990000000000009094947017729282379150390625000000000000000000000000000000000000000000000000000000000e+000");
assert_eq(agh.sprintf("%%f: %f %#g %#f %#.g %f %'f", 1, 1, 1, 1, 1e100, 1e100),
          "%f: 1.000000 1.00000 1.000000 1."
          + " 9999999999999998578914528479799628257751464843750000000000000000000000000000000000000000000000000000.000000"
          + " 9,999,999,999,999,998,578,914,528,479,799,628,257,751,464,843,750,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000.000000");
assert_eq(agh.sprintf("%%g: %.15g %.15g %#.15g", 1, 1.2, 1.2), "%g: 1 1.2 1.20000000000000");
assert_eq(agh.sprintf("%%g: %g %.g %#g %#.g", 15, 15, 15, 15), "%g: 15 2e+001 15.0000 2.e+001");
assert_eq(agh.sprintf("%%g: %g %g %g %g %g", 1e-1, 1e-3, 1e-4, 1e-5, 9e-5, 9e-4, 1e10), "%g: 0.1 0.001 0.0001 1e-005 9e-005");
assert_eq(agh.sprintf("%%#g: %#g %#g %#g %#2g %#6g", 0.1, 1e-5, 1e-4, 1e-4, 1e-4), "%#g: 0.100000 1.00000e-005 0.000100000 0.000100000 0.000100000");
assert_eq(agh.sprintf("%%#.g: %#.2g %#.2g", 1e-4, 1e-5), "%#.g: 0.00010 1.0e-005");
assert_eq(agh.sprintf("%%.g: %.g %.g %.g; %.1g %.1g %.1g; %.2g %.3g", 0.1, 0.999, 9.999, 9, 9.9, 9.999, 9.999, 9.999), "%.g: 0.1 1. 1e+001; 9 1e+001 1e+001; 10. 10");

assert_eq(agh.sprintf("%%c: [%c][%c][%c]\n", 1e100, 65, 8), "%c: [\0][A][\b]\n");
assert_eq(agh.sprintf("%05s %05s\n", 123, "aaa"), "00123 00aaa\n");
assert_eq(agh.sprintf("%%p: %p", 512), "%p: 0x200");
assert_eq(agh.sprintf("pi: [%1$a][%1$g][%1$'20.9g][%1$020.9g][%1$'020.9g][%2$'020.9g]", pi, pi * 1e3),
          "pi: [0x1.921fb54442d18p+001][3.14159][          3.14159265][00000000003.14159265][00000000003.14159265][0000000003,141.59265]");
