---
title: "CF 102189G - \u041f\u0438\u0440\u043e\u0433"
description: "We have a rectangle of width A and height B. A single point inside it is connected to all four corners, producing four triangular pieces."
date: "2026-08-19T06:22:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102189
codeforces_index: "G"
codeforces_contest_name: "12-\u0439 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u0442\u0443\u0440\u043d\u0438\u0440 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e \u0432 \u0410\u0431\u0430\u043a\u0430\u043d\u0435"
rating: 0
weight: 102189
solve_time_s: 87
verified: true
draft: false
---

[CF 102189G - \u041f\u0438\u0440\u043e\u0433](https://codeforces.com/problemset/problem/102189/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
# Problem Understanding

We have a rectangle of width A and height B. A single point inside it is connected to all four corners, producing four triangular pieces. The four guests request percentages p 1 ​ ,p 2 ​ ,p 3 ​ ,p 4 ​ of the total area, and the task is to decide whether some placement of the point can produce exactly those four areas.

The guests are not tied to particular corners, so we are free to assign the four requested percentages to the four triangular pieces in any order. If such an assignment exists, we output the corresponding coordinates X,Y. Since every p i ​ is positive, every required piece has positive area, so a valid point will automatically be strictly inside the rectangle.

The rectangle dimensions are at most 100, while there are always exactly four percentages. The small dimensions make numerical brute force possible, but geometry gives us a constant-time solution that does not depend on the size of the rectangle at all. There are only 4!=24 possible ways to place the four percentages around the rectangle, so checking all of them is effectively constant time.

The main edge case is that equal or similar-looking percentages do not automatically form a valid configuration. For example,

```
1 133 33 33 1
```

must produce `NO`. A careless approach might try to put the three 33% pieces next to each other and assume that a point can realize any four positive areas summing to 100%. The four areas created by one point satisfy an additional multiplicative relation, so the sum condition alone is insufficient.

Another subtle case is equal pieces:

```
3 425 25 25 25
```

The correct output is `YES`, with the center (1.5,2) being one valid answer. A solution that only considers integer coordinates would incorrectly reject this case because the required X coordinate is fractional.

A third case is a valid configuration with all coordinates fractional:

```
10 206 24 56 14
```

The correct answer is `YES`, with X=2 and Y=6. Trying only the midpoint or only integer percentages of the dimensions would miss the general construction.

# Approaches

A direct numerical approach could enumerate possible normalized coordinates x=X/A and y=Y/B, compute the four resulting areas, and compare them with the requested percentages under all assignments. Because the percentages are integers, a valid solution has x and y with denominator at most 100, so checking a grid of 101 by 101 normalized coordinates is enough. Combining that with all 24 assignments takes at most 101 2 ⋅24=244,824 checks, which is actually fast enough for these constraints.

The problem with that approach is not performance here, but that the grid argument is easy to get wrong. A generic floating-point grid does not give a mathematical guarantee, and enumerating coordinates with arbitrary precision quickly becomes expensive. For example, a grid with 10 6 possible values for each coordinate would require about 10 12 coordinate pairs, or about 2.4⋅10 13 comparisons after considering all assignments. More importantly, there is no reason to approximate a problem whose conditions can be checked exactly.

The key observation comes from writing the four triangle areas in terms of normalized coordinates. Set

x= A X ​ ,y= B Y ​ .

Suppose the four percentages, expressed as fractions of the whole rectangle, are arranged cyclically as q 1 ​ ,q 2 ​ ,q 3 ​ ,q 4 ​, starting from the lower-left triangle and going around the rectangle. Their areas divided by the rectangle area are

q 1 ​ =xy,
q 2 ​ =(1−x)y,
q 3 ​ =(1−x)(1−y),
q 4 ​ =x(1−y).

From these equations,

q 1 ​ q 3 ​ =xy(1−x)(1−y)

and

q 2 ​ q 4 ​ =(1−x)yx(1−y),

so necessarily

q 1 ​ q 3 ​ =q 2 ​ q 4 ​ .

This condition is also sufficient. If four positive percentages satisfy that equality and sum to 1, then

y=q 1 ​ +q 2 ​

and

x=q 1 ​ +q 4 ​

produce exactly those four areas.

Since the guests can be assigned to corners in any order, we simply test all 24 permutations and look for one satisfying the product equality. Everything can be done with integers, using p 1 ​ p 3 ​ =p 2 ​ p 4 ​, so there is no floating-point precision issue.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Coordinate grid | O(101 2 ⋅4!) | O(1) | Accepted, but unnecessary |
| Permutation + area identity | O(4!)=O(1) | O(1) | Accepted |

# Algorithm Walkthrough

1. Read A,B and the four requested percentages.
2. Generate every permutation of the four percentages. A permutation represents assigning the percentages to the four triangles in cyclic order around the chosen point.
3. For a permutation (q 1 ​ ,q 2 ​ ,q 3 ​ ,q 4 ​ ), test whether

q 1 ​ q 3 ​ =q 2 ​ q 4 ​ .

This is exactly the multiplicative identity forced by four triangles meeting at one point. Because all values are integers, the comparison is exact.

1. If the identity fails, try the next permutation. If it succeeds, recover the normalized coordinates from the sums of adjacent pieces:

x=q 1 ​ +q 4 ​ ,y=q 1 ​ +q 2 ​ ,

where the percentages are interpreted as fractions, so the actual values are

x= 100 q 1 ​ +q 4 ​ ​ ,y= 100 q 1 ​ +q 2 ​ ​ .

1. Convert normalized coordinates back to the original rectangle:

X=A 100 q 1 ​ +q 4 ​ ​ ,Y=B 100 q 1 ​ +q 2 ​ ​ .

Output `YES`, followed by these two coordinates.

1. If all 24 permutations fail the product identity, output `NO`. No valid placement can exist because every possible assignment of the requested pieces to the four corners has been rejected.

### Why it works

For every possible placement of the point, the four normalized triangle areas have the form xy,(1−x)y,(1−x)(1−y),x(1−y), so opposite products are always equal. Thus every valid arrangement must pass the tested identity. Conversely, suppose a permutation passes the identity. Set x=(q 1 ​ +q 4 ​ )/100 and y=(q 1 ​ +q 2 ​ )/100. The sum condition and the product identity give q 1 ​ =100xy, q 2 ​ =100(1−x)y, q 3 ​ =100(1−x)(1−y), and q 4 ​ =100x(1−y). Hence the constructed point produces exactly the four requested areas. Since all percentages are positive and sum to 100, both coordinates lie strictly between the rectangle's boundaries.

# Python Solution

```python
Pythonimport sysimport itertools
input = sys.stdin.readline

def solve():    A, B = map(int, input().split())    p = list(map(int, input().split()))
    for q1, q2, q3, q4 in itertools.permutations(p):        if q1 * q3 != q2 * q4:            continue
        X = A * (q1 + q4) / 100.0        Y = B * (q1 + q2) / 100.0
        print("YES")        print(X)        print(Y)        return
    print("NO")

if __name__ == "__main__":    solve()
```

The permutation loop corresponds directly to assigning the four guests to the four triangular pieces in cyclic order. There are only 24 permutations, and duplicates among equal percentages cause no correctness problem because testing the same arrangement more than once is harmless.

The product comparison uses the original integer percentages rather than floating-point fractions. Multiplying by 100 cancels from both sides, giving exactly q 1 ​ q 3 ​ =q 2 ​ q 4 ​. This avoids all issues with values such as 0.33 that cannot be represented exactly in binary floating point.

Once a valid permutation is found, q 1 ​ +q 4 ​ is the fraction of the rectangle lying to the left of the point. Thus it equals X/A. Similarly, q 1 ​ +q 2 ​ is the fraction lying below the point, so it equals Y/B. Multiplication by A and B gives the actual coordinates.

Python's floating-point output is sufficient here because the judge accepts coordinates with numerical precision. The underlying existence test is completely exact, so floating-point arithmetic is used only for the final presentation of coordinates.

# Worked Examples

## Sample 1

The input is

```
3 425 25 25 25
```

The first permutation already has the required opposite-product equality.

| Step | q 1 ​ | q 2 ​ | q 3 ​ | q 4 ​ | q 1 ​ q 3 ​ | q 2 ​ q 4 ​ | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Check permutation | 25 | 25 | 25 | 25 | 625 | 625 | Valid |
| Compute X | 25 | 25 | 25 | 25 |  |  | 3⋅50/100=1.5 |
| Compute Y | 25 | 25 | 25 | 25 |  |  | 4⋅50/100=2 |

The point is (1.5,2). Each triangle has area 3⋅4/4=3, exactly 25% of the rectangle.

## Sample 2

The input is

```
1 133 33 33 1
```

For any permutation, the value 1 occupies one position and the three values 33 occupy the other positions. The opposite products can only be 33⋅33=1089 on one side and 33⋅1=33 on the other, or the same values in reverse positions.

| Arrangement type | q 1 ​ q 3 ​ | q 2 ​ q 4 ​ | Result |
| --- | --- | --- | --- |
| 1 opposite 33 | 33 | 1089 | Invalid |
| 33 opposite 1 | 1089 | 33 | Invalid |

No permutation satisfies the necessary identity, so the algorithm prints `NO`. The trace demonstrates why four positive areas summing to 100% are not sufficient to guarantee that one point can generate them.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(4!)=O(1) | At most 24 permutations are checked, with constant-time arithmetic for each |
| Space | O(1) | Only the four percentages and a constant amount of temporary data are stored |

The rectangle dimensions can be as large as 100, but they do not affect the number of cases examined. The algorithm performs only a few dozen integer multiplications and additions, so it is comfortably within the 1 second time limit and uses negligible memory.

# Test Cases

The test harness below checks the structural properties of the answer rather than requiring one particular valid coordinate, because the problem allows any valid placement. It runs the same solution logic and validates the produced coordinates by reconstructing the four triangle percentages.

```python
Pythonimport sysimport ioimport itertools

def solve_case(inp: str) -> str:    old_stdin = sys.stdin    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)    out = io.StringIO()    sys.stdout = out
    try:        A, B = map(int, sys.stdin.readline().split())        p = list(map(int, sys.stdin.readline().split()))
        for q1, q2, q3, q4 in itertools.permutations(p):            if q1 * q3 != q2 * q4:                continue
            X = A * (q1 + q4) / 100.0            Y = B * (q1 + q2) / 100.0
            print("YES")            print(X)            print(Y)            return out.getvalue()
        print("NO")        return out.getvalue()    finally:        sys.stdin = old_stdin        sys.stdout = old_stdout

def run(inp: str) -> str:    return solve_case(inp)

def parse_valid_output(inp: str, output: str) -> bool:    lines = output.strip().splitlines()    if lines[0] == "NO":        return False
    assert lines[0] == "YES"    X = float(lines[1])    Y = float(lines[2])
    first, second = inp.strip().splitlines()    A, B = map(float, first.split())    p = list(map(int, second.split()))
    x = X / A    y = Y / B
    areas = [        100.0 * x * y,        100.0 * (1.0 - x) * y,        100.0 * (1.0 - x) * (1.0 - y),        100.0 * x * (1.0 - y),    ]
    remaining = areas[:]    for value in p:        found = False        for i, area in enumerate(remaining):            if abs(area - value) < 1e-7:                remaining.pop(i)                found = True                break        if not found:            return False
    return -1e-9 <= x <= 1.0 + 1e-9 and -1e-9 <= y <= 1.0 + 1e-9

# Provided samplesassert parse_valid_output(    "3 4\n25 25 25 25\n",    run("3 4\n25 25 25 25\n")), "sample 1"
assert run("1 1\n33 33 33 1\n").strip() == "NO", "sample 2"

# Minimum-size rectangle and equal piecesassert parse_valid_output(    "1 1\n25 25 25 25\n",    run("1 1\n25 25 25 25\n")), "minimum rectangle"

# A non-symmetric valid configurationassert parse_valid_output(    "10 20\n6 24 56 14\n",    run("10 20\n6 24 56 14\n")), "valid asymmetric case"

# Maximum-size rectangle with a valid configurationassert parse_valid_output(    "100 100\n6 24 56 14\n",    run("100 100\n6 24 56 14\n")), "maximum rectangle"

# A case close to the invalid sample, catching incorrect sum-only logicassert run("100 1\n40 30 20 10\n").strip() == "NO", "invalid product relation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 25 25 25 25` | `YES` | Minimum dimensions and fractional coordinates |
| `10 20 / 6 24 56 14` | `YES` | General asymmetric valid configuration |
| `100 100 / 6 24 56 14` | `YES` | Maximum dimensions |
| `100 1 / 40 30 20 10` | `NO` | Product condition rather than merely the sum of percentages |

# Edge Cases

For

```
1 125 25 25 25
```

the first permutation passes because 25⋅25=25⋅25. The coordinate formulas give X=1(25+25)/100=0.5 and Y=1(25+25)/100=0.5. The algorithm accepts the center, showing why integer-coordinate enumeration would be incorrect.

For

```
1 133 33 33 1
```

every permutation has one opposite-product side equal to 33⋅33 and the other equal to 33⋅1. Since 1089  =33, every permutation is rejected and the output is `NO`. This catches the mistake of assuming that arbitrary positive percentages summing to 100 can be realized.

For

```
10 206 24 56 14
```

the given order itself works because

6⋅56=336

and

24⋅14=336.

The coordinate calculation gives

X=10⋅ 100 6+14 ​ =2

and

Y=20⋅ 100 6+24 ​ =6.

The four normalized areas are 0.06,0.24,0.56,0.14, exactly matching the requested percentages.

For

```
100 140 30 20 10
```

the dimensions themselves do not matter to the existence test. The algorithm checks all 24 arrangements, but no arrangement satisfies the opposite-product equality. For example, the natural order gives 40⋅20=800 and 30⋅10=300. Other permutations merely choose different opposite pairs, and none has equal products. The correct result is `NO`, demonstrating that changing the rectangle dimensions cannot rescue an impossible set of four percentages.
