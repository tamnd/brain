---
title: "CF 102297B - Medal Ranking"
description: "Each test case describes the medal counts of two countries, USA and Russia. The six integers are ordered as USA gold, silver, bronze, followed by Russia gold, silver, bronze. There are two independent ways to decide whether USA wins."
date: "2026-08-13T22:42:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102297
codeforces_index: "B"
codeforces_contest_name: "UCF Locals 2015"
rating: 0
weight: 102297
solve_time_s: 58
verified: true
draft: false
---

[CF 102297B - Medal Ranking](https://codeforces.com/problemset/problem/102297/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes the medal counts of two countries, USA and Russia. The six integers are ordered as USA gold, silver, bronze, followed by Russia gold, silver, bronze.

There are two independent ways to decide whether USA wins. Under the `count` ranking, only the total number of medals matters, so we compare the sums of the three medal counts. Under the `color` ranking, medal types have a strict priority: gold is compared first, silver is considered only when gold is tied, and bronze is considered only when both gold and silver are tied. This is exactly a lexicographic comparison of the triples `(gold, silver, bronze)`.

For every test case, we print the original six numbers, then print `count` if USA wins only by total medals, `color` if USA wins only by medal color, `both` if USA wins under both systems, and `none` if Russia is not beaten under either system. A blank line follows each result.

The statement specifies a positive number `n` of test cases and says each medal count is between `0` and `500`. Those bounds make every arithmetic operation tiny. Even if `n` were as large as `10^5` or more, there is no need for sorting, dynamic programming, graph traversal, or any operation depending on the medal values. We perform a constant amount of work per test case, so the total work grows linearly with the number of cases.

The supplied sample in the statement contains the five six-integer test cases but does not show the leading `n`, despite the written input description saying that `n` should be present. The solution below accepts both forms: the official `n`-prefixed format and the sample's six-integer-per-case format. This does not change the algorithm or its complexity.

A common edge case is a tie in total medals while USA wins by color. For example,

```
1
10 5 5 8 6 6
```

USA has `20` medals and Russia has `20`, so USA does not win by count. However, USA has more gold medals, `10` versus `8`, so the correct result is `color`. A careless solution that decides the answer from the total medal count alone would incorrectly reject USA's color win.

The reverse situation is also possible. For example,

```
1
8 5 5 10 4 3
```

USA has `18` medals while Russia has `17`, so USA wins by count. Russia has more gold medals, however, `10` versus `8`, so USA loses the color ranking. The correct result is `count`. A solution that treats the two ranking systems as equivalent would get this case wrong.

Another subtle case is a tie in gold that must be resolved using silver. For example,

```
1
5 8 1 5 7 10
```

Both countries have five gold medals, so gold cannot decide the color ranking. USA has eight silver medals compared with Russia's seven, so USA wins by color. Bronze is irrelevant once silver breaks the tie.

The same logic applies one level deeper when both gold and silver are tied. For example,

```
1
5 7 9 5 7 8
```

The gold counts are equal and the silver counts are equal, so bronze decides the color ranking. USA has nine bronze medals versus Russia's eight, giving USA the color win.

Finally, an exact tie under both systems must produce `none`, not a win. For example,

```
1
5 7 9 5 7 9
```

Both the total counts and all three medal colors are identical, so neither comparison is strictly greater.

## Approaches

A straightforward approach is to calculate USA's total and Russia's total, then compare the three medal counts one at a time for the color ranking. This is already enough to solve the problem because there are only six input values per test case. The total comparison needs two additions, and the color comparison needs at most three comparisons.

One might describe an even more literal brute-force strategy as checking every possible ordering of the three medal colors and trying to determine which ordering matches the ranking rule. There are only `3! = 6` such orderings, so even that approach performs at most a constant number of operations per case. With `n` test cases, the worst case is roughly `6n` ordering checks, which is still `O(n)`. There is no realistic input size for which this becomes too slow under the stated constraints. The problem is fixed-size enough that the useful optimization is not an asymptotic improvement, but recognizing that no search or sorting is necessary in the first place.

The key observation is that the color ranking is already fully described by the order `(gold, silver, bronze)`. We do not need to construct a ranking, sort the medals, or assign weights to the medal types. We simply compare the two triples lexicographically. Python's tuple comparison expresses exactly this rule, although the solution can also write the three comparisons explicitly to make the reasoning transparent.

The brute-force idea works because the amount of data in one case is constant, but it introduces unnecessary work by considering possibilities that the problem has already ordered for us. The observation that color ranking is a direct lexicographic comparison reduces the entire task to two constant-time predicates, one for total count and one for color.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted, but unnecessary work |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the six medal counts for one test case and keep them in the original order. Printing these values unchanged is part of the required output, so there is no reason to reconstruct the input later.
2. Compute USA's total medals as `ug + us + ub` and Russia's total as `rg + rs + rb`. Set `wins_count` according to whether USA's total is strictly larger. Equality is not a win because the statement asks whether USA wins, not whether USA ties.
3. Compare the medal triples `(ug, us, ub)` and `(rg, rs, rb)` in gold, silver, bronze order. USA wins the color ranking if its gold count is larger, or if gold is tied and its silver count is larger, or if both gold and silver are tied and its bronze count is larger.
4. Combine the two boolean results. If both are true, print `both`. If only the count result is true, print `count`. If only the color result is true, print `color`. If neither is true, print `none`.
5. Print a blank line after the result of the test case. This matches the required output structure and also keeps consecutive test cases visually separated.

The key invariant is that after the total comparison, `wins_count` is true exactly when USA has strictly more medals overall. After the color comparison, `wins_color` is true exactly when the first medal type at which the countries differ belongs to USA and has a larger count. Since every possible outcome is determined by these two independent predicates, the final four-way classification cannot be wrong.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))

    if not data:
        return

    # The written statement includes n, while the supplied sample
    # omits it. Support both formats.
    if len(data) >= 1 and (len(data) - 1) % 6 == 0 and data[0] == (len(data) - 1) // 6:
        n = data[0]
        start = 1
    else:
        n = len(data) // 6
        start = 0

    out = []

    for i in range(n):
        a = data[start + 6 * i:start + 6 * i + 6]
        ug, us, ub, rg, rs, rb = a

        usa_total = ug + us + ub
        russia_total = rg + rs + rb
        wins_count = usa_total > russia_total

        if ug != rg:
            wins_color = ug > rg
        elif us != rs:
            wins_color = us > rs
        else:
            wins_color = ub > rb

        if wins_count and wins_color:
            result = "both"
        elif wins_count:
            result = "count"
        elif wins_color:
            result = "color"
        else:
            result = "none"

        out.append(" ".join(map(str, a)))
        out.append(result)
        out.append("")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The program first reads all integers at once. This avoids depending on whether the test cases are physically arranged one per line, because whitespace is the only relevant separator for integer input.

The format detection handles the discrepancy between the written statement and the supplied sample. If the first number equals the number of remaining groups of six integers, it is interpreted as `n`. Otherwise, all integers are treated as medal data. Under the official format, an input beginning with `5` followed by thirty medal values is recognized as five cases. Under the supplied sample format, thirty medal values are recognized as five cases.

For each case, the six values are unpacked into the three USA counts and three Russia counts. The total ranking uses ordinary integer addition and a strict `>` comparison.

The color ranking is deliberately written as explicit conditional comparisons instead of relying on tuple syntax. If gold differs, the decision is made immediately because silver and bronze no longer matter. If gold is tied, silver gets the same treatment. Only when both are tied do we compare bronze. This directly mirrors the ranking rule and avoids accidentally treating medal types as equally valuable.

The final conditional chain handles the four possible combinations of the two rankings. There is no integer overflow concern in Python, and even in a fixed-width language the maximum total is only `1500`, since each country has three medal counts of at most `500`.

## Worked Examples

### Sample 1

Consider the first supplied case:

```
10 5 15 10 1 0
```

The key state changes are:

| USA `(G,S,B)` | Russia `(G,S,B)` | USA Total | Russia Total | Count Win | Color Win | Result |
| --- | --- | --- | --- | --- | --- | --- |
| `(10,5,15)` | `(10,1,0)` | 30 | 11 | true | true | both |

The total comparison gives USA `30` medals against Russia's `11`, so USA wins by count. Gold is tied at `10`, so the color comparison moves to silver. USA has five silver medals against Russia's one, so USA also wins by color. The final classification is `both`.

### Sample 2

The second supplied case is:

```
10 5 15 10 6 10
```

The state is:

| USA `(G,S,B)` | Russia `(G,S,B)` | USA Total | Russia Total | Count Win | Color Win | Result |
| --- | --- | --- | --- | --- | --- | --- |
| `(10,5,15)` | `(10,6,10)` | 30 | 26 | true | false | count |

USA still has more total medals, `30` versus `26`, so the count comparison is true. Gold is tied at `10`, but Russia has six silver medals while USA has five. Silver breaks the color comparison, so USA loses by color. The answer is consequently `count`.

These two examples demonstrate why the two ranking systems must be evaluated independently. The first reaches `both`, while the second reaches `count` even though the gold counts are identical.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each of the `n` test cases performs a fixed number of arithmetic operations and comparisons. |
| Space | O(n) | The implementation stores the complete input and output strings, so its actual memory usage grows linearly with the input size. The algorithmic working space for one case is O(1). |

With only six integers per test case and a constant amount of computation per case, the processing itself is easily fast enough for the stated constraints. The medal counts are at most `500`, so the arithmetic is trivial. The only linear memory comes from the convenient whole-input and buffered-output implementation, not from the algorithm's reasoning.

If a strict streaming implementation were preferred, the working memory could be reduced to `O(1)` beyond the output buffer by reading one test case at a time.

## Test Cases

```python
import sys
import io

def solve_data(data: str) -> str:
    values = list(map(int, data.split()))

    if not values:
        return ""

    if len(values) >= 1 and (len(values) - 1) % 6 == 0 \
            and values[0] == (len(values) - 1) // 6:
        n = values[0]
        start = 1
    else:
        n = len(values) // 6
        start = 0

    out = []

    for i in range(n):
        a = values[start + 6 * i:start + 6 * i + 6]
        ug, us, ub, rg, rs, rb = a

        wins_count = ug + us + ub > rg + rs + rb

        if ug != rg:
            wins_color = ug > rg
        elif us != rs:
            wins_color = us > rs
        else:
            wins_color = ub > rb

        if wins_count and wins_color:
            result = "both"
        elif wins_count:
            result = "count"
        elif wins_color:
            result = "color"
        else:
            result = "none"

        out.append(" ".join(map(str, a)))
        out.append(result)
        out.append("")

    return "\n".join(out)

def run(inp: str) -> str:
    return solve_data(inp)

sample = """10 5 15 10 1 0
10 5 15 10 6 10
12 5 10 5 20 30
10 0 15 10 5 30
10 5 15 10 5 15
"""

sample_expected = """10 5 15 10 1 0
both
10 5 15 10 6 10
count
12 5 10 5 20 30
color
10 0 15 10 5 30
none
10 5 15 10 5 15
none
"""

assert run(sample) == sample_expected, "provided sample"

sample_with_n = """5
10 5 15 10 1 0
10 5 15 10 6 10
12 5 10 5 20 30
10 0 15 10 5 30
10 5 15 10 5 15
"""

assert run(sample_with_n) == sample_expected, "official n-prefixed format"

minimum = """1
0 0 0 0 0 0
"""

assert run(minimum) == """0 0 0 0 0 0
none
""", "minimum and complete tie"

maximum = """1
500 500 500 499 499 499
"""

assert run(maximum) == """500 500 500 499 499 499
both
""", "maximum medal counts"

all_equal = """1
10 20 30 10 20 30
"""

assert run(all_equal) == """10 20 30 10 20 30
none
""", "all values equal"

gold_tie_silver_win = """1
5 8 1 5 7 10
"""

assert run(gold_tie_silver_win) == """5 8 1 5 7 10
color
""", "silver breaks a gold tie"

count_only = """1
8 5 5 10 4 3
"""

assert run(count_only) == """8 5 5 10 4 3
count
""", "count wins while color loses"

bronze_breaks_tie = """1
5 7 9 5 7 8
"""

assert run(bronze_breaks_tie) == """5 7 9 5 7 8
color
""", "bronze breaks gold and silver ties"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0 0 0 0` | `none` | Minimum values and exact equality |
| `500 500 500 499 499 499` | `both` | Maximum values and both rankings |
| `10 20 30 10 20 30` | `none` | Complete equality across all medal types |
| `5 8 1 5 7 10` | `color` | Silver comparison after a gold tie |
| `8 5 5 10 4 3` | `count` | Count win while color ranking is lost |
| `5 7 9 5 7 8` | `color` | Bronze comparison after gold and silver ties |

## Edge Cases

The first edge case is an exact tie. For

```
1
5 7 9 5 7 9
```

both totals are `21`, so `wins_count` is false. Gold is tied, silver is tied, and bronze is also tied, so the final color comparison is `9 > 9`, which is false. Both predicates are false, giving `none`. A non-strict comparison such as `>=` would incorrectly classify this as a USA win.

A tie in total medals does not prevent a color win. For

```
1
10 5 5 8 6 6
```

both countries have `20` medals, so the count comparison fails. Gold decides the color ranking immediately because `10 > 8`, giving `color`. The algorithm never needs to inspect silver or bronze once gold differs.

The opposite case is also possible. For

```
1
8 5 5 10 4 3
```

USA has `18` medals and Russia has `17`, so count is a USA win. Gold goes the other way, `8 < 10`, so color is a loss. The two booleans become `true` and `false`, producing `count`.

When gold is tied, silver must be checked before bronze. For

```
1
5 8 1 5 7 10
```

the gold comparison is inconclusive because both values are `5`. Silver gives USA the win with `8 > 7`, so the result is `color`. A careless implementation that compares only gold and declares a tie would miss this win.

When both gold and silver are tied, bronze becomes decisive. For

```
1
5 7 9 5 7 8
```

the first two comparisons are equal, but USA has nine bronze medals versus Russia's eight. The color predicate is true, producing `color`.

Finally, the maximum values

```
1
500 500 500 499 499 499
```

give USA `1500` medals against Russia's `1497`, and USA also has more gold medals. Both predicates are true, so the result is `both`. This confirms that the arithmetic and comparisons behave normally at the upper boundary of the stated medal-count range.
