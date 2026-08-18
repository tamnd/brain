---
title: "CF 102203A - \u0414\u043e\u0431\u0440\u043e \u043f\u043e\u0436\u0430\u043b\u043e\u0432\u0430\u0442\u044c \u043d\u0430 \u0424\u043b\u043e\u0440\u0438\u043d\u0443!"
description: "We have two binary reports about deliveries to n planets. For each planet, the first report tells us whether both kinds of kryt are delivered there. The second report tells us whether at least one kind is delivered there."
date: "2026-08-18T11:17:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102203
codeforces_index: "A"
codeforces_contest_name: "\u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e (8-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 102203
solve_time_s: 49
verified: true
draft: false
---

[CF 102203A - \u0414\u043e\u0431\u0440\u043e \u043f\u043e\u0436\u0430\u043b\u043e\u0432\u0430\u0442\u044c \u043d\u0430 \u0424\u043b\u043e\u0440\u0438\u043d\u0443!](https://codeforces.com/problemset/problem/102203/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two binary reports about deliveries to `n` planets. For each planet, the first report tells us whether both kinds of kryt are delivered there. The second report tells us whether at least one kind is delivered there.

We need a third binary report where position `i` is `1` exactly when the planet receives one kind of kryt but not both. In other words, we need to distinguish the planets receiving exactly one type from the planets receiving either both types or none.

For a single planet, let the two actual delivery indicators be `a` and `b`. The first report contains `a AND b`, while the second contains `a OR b`. The desired value is `1` when exactly one of `a` and `b` is `1`, which is precisely the XOR operation. Since `a AND b` is already given by the first report and `a OR b` by the second, the desired value is simply `S1[i] XOR S2[i]`.

The constraint `n <= 10^5` means the input itself contains only about `10^5` characters, so an algorithm that processes every position once is easily fast enough. An algorithm with quadratic work would already perform around `10^10` operations at the maximum size and would not fit a one-second limit. Exponential algorithms are vastly beyond the feasible range.

The first edge case is a planet where neither type is delivered. For example,

```
1
0
0
```

The answer is `0`. A careless approach that interprets the second report's zero as somehow indicating a difference would be wrong, because there is no delivery at all.

The second edge case is a planet where both types are delivered:

```
1
1
1
```

The answer is again `0`. The first report already tells us that both types are present, so this planet must not appear in the requested report. Using only the second report would incorrectly produce `1`.

A third useful case has adjacent positions with different situations:

```
4
0101
1111
```

The answer is `1010`. At positions where the reports differ, exactly one type is delivered. At positions where they agree, either both types or neither type is delivered.

## Approaches

A completely brute-force solution could imagine every possible delivery configuration for the two types on all `n` planets. There are two binary decisions per planet, so there are `2^(2n) = 4^n` possible configurations. For each configuration, we could construct its two reports, compare them with the input, and output the corresponding answer if they match. This is logically correct because it considers every possible underlying delivery assignment, but at `n = 10^5` the number of configurations is `4^100000`, which is incomprehensibly large.

The brute-force works because it searches the entire space of possible delivery states, but that search is unnecessary because every planet is independent of every other planet. We do not need to reconstruct the actual two delivery sets. For one position, the first report says whether the two delivery bits are simultaneously `1`, and the second says whether at least one is `1`. Those two pieces of information completely determine whether exactly one is present.

The key observation is that `S1[i]` is `a AND b` and `S2[i]` is `a OR b`. Exactly one of `a` and `b` is true precisely when these two values differ. Thus the answer at every position is `S1[i] XOR S2[i]`. We can scan the two strings once and produce the answer character by character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(4^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n` and the two binary strings `S1` and `S2`. Each character at index `i` describes the same planet in both reports.
2. Create an empty result string. We will append one character for each planet, so the result will have exactly `n` characters.
3. For every position `i` from `0` through `n - 1`, compare `S1[i]` and `S2[i]`. If they are equal, append `0`. If they are different, append `1`.

The reason is that equality means either both types are delivered or neither type is delivered. A difference means one report says "both" while the other says "at least one", which can happen only when exactly one type is delivered.
4. Print the resulting binary string.

### Why it works

For every planet, let `a` and `b` denote whether the two types of kryt are delivered. The first report contains `a AND b`, and the second contains `a OR b`. If both `a` and `b` are zero, both report values are zero. If both are one, both report values are one. If exactly one is one, the AND value is zero and the OR value is one. Therefore the desired answer is `1` exactly when the two report characters differ, which is exactly `S1[i] XOR S2[i]`. Since this reasoning holds independently for every position, the complete constructed string is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s1 = input().strip()
    s2 = input().strip()

    ans = ''.join('1' if a != b else '0' for a, b in zip(s1, s2))
    print(ans)

if __name__ == "__main__":
    solve()
```

The first three input operations read the number of planets and the two reports. `strip()` removes the newline without changing any meaningful binary characters.

The `zip(s1, s2)` expression pairs the reports position by position. For each pair, the conditional expression produces `1` when the characters differ and `0` when they are equal, exactly implementing XOR for binary characters.

Using `join` builds the entire answer string efficiently. There is no need for integer conversion, bit masks, or explicit indexing, and there are no boundary calculations beyond the fact that both strings have length `n`.

The variable `n` is read because it is part of the input format, although the construction itself can safely rely on the two strings having the required length. Python integers have no overflow issue here, and the algorithm performs only linear work.

## Worked Examples

The statement excerpt provided here does not contain actual sample input and output values, so the following traces use two small inputs that exercise the two possible situations.

### Example 1

```
4
0101
1111
```

The two reports are processed as follows.

| Position | `S1[i]` | `S2[i]` | Different? | Answer character |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | Yes | 1 |
| 1 | 1 | 1 | No | 0 |
| 2 | 0 | 1 | Yes | 1 |
| 3 | 1 | 1 | No | 0 |

The resulting answer is `1010`. Positions `0` and `2` have at least one delivery but not both, while positions `1` and `3` have both types.

### Example 2

```
5
00000
10101
```

| Position | `S1[i]` | `S2[i]` | Different? | Answer character |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | Yes | 1 |
| 1 | 0 | 0 | No | 0 |
| 2 | 0 | 1 | Yes | 1 |
| 3 | 0 | 0 | No | 0 |
| 4 | 0 | 1 | Yes | 1 |

The resulting answer is `10101`. Since the first report contains no position where both types are delivered, every `1` in the second report directly represents a planet receiving exactly one type.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every position of the two reports is examined once. |
| Space | O(n) | The resulting binary string contains `n` characters. |

With `n <= 10^5`, the algorithm performs only a linear number of character operations. The input and output themselves are already of size `O(n)`, so this is asymptotically optimal because we must at least read the reports and produce the answer.

## Test Cases

The supplied statement excerpt has no actual sample values, so the test suite below uses the two worked examples above as representative samples and adds cases for the smallest input, equal reports, the maximum input size, and alternating boundaries.

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    s1 = input().strip()
    s2 = input().strip()

    ans = ''.join('1' if a != b else '0' for a, b in zip(s1, s2))
    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_input = sys.stdin.readline

    try:
        sys.stdin = io.StringIO(inp)
        return_value = io.StringIO()

        old_stdout = sys.stdout
        sys.stdout = return_value
        try:
            solve()
        finally:
            sys.stdout = old_stdout

        return return_value.getvalue().strip()
    finally:
        sys.stdin = old_stdin

# Worked example 1
assert run("4\n0101\n1111\n") == "1010", "worked example 1"

# Worked example 2
assert run("5\n00000\n10101\n") == "10101", "worked example 2"

# Minimum-size input
assert run("1\n0\n0\n") == "0", "minimum size"

# Both reports are identical, so every position is 0
assert run("6\n101010\n101010\n") == "000000", "identical reports"

# Maximum-size input
n = 100000
s1 = "0" * n
s2 = "1" * n
assert run(f"{n}\n{s1}\n{s2}\n") == "1" * n, "maximum size"

# Boundary and alternating positions
assert run("8\n00110011\n01100110\n") == "01010101", "alternating differences"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 / 0101 / 1111` | `1010` | Mixed positions where the reports agree and disagree |
| `5 / 00000 / 10101` | `10101` | Cases where no planet receives both types |
| `1 / 0 / 0` | `0` | Minimum input size and the no-delivery case |
| `6 / 101010 / 101010` | `000000` | Both reports identical, so no planet receives exactly one type |
| `100000 / 000...0 / 111...1` | `111...1` | Maximum input size and linear-time behavior |
| `8 / 00110011 / 01100110` | `01010101` | Alternating differences and boundary positions |

## Edge Cases

The no-delivery case is represented by equal zeroes. For example,

```
1
0
0
```

At the only position, `S1[0]` and `S2[0]` are equal, so the algorithm appends `0`. The output is `0`, correctly indicating that neither type is delivered.

The both-types case is represented by equal ones:

```
1
1
1
```

Here the two reports again agree, so the algorithm produces `0`. The first report says that both types are present, while the second confirms that at least one is present. Since the requested report contains only planets with exactly one type, this planet must be excluded.

A case where the reports differ demonstrates the positive condition:

```
1
0
1
```

The first report says both types are not simultaneously delivered, while the second says at least one type is delivered. The only possible situation is that exactly one type is delivered, so the algorithm compares `0` and `1`, sees a difference, and outputs `1`.

The maximum-size case has the same logic at every position. If `n = 100000`, `S1` consists of `100000` zeroes and `S2` consists of `100000` ones, every pair differs, so the answer is `100000` ones. The algorithm performs one comparison per position and never needs nested loops, so the large input remains comfortably within the intended linear complexity.
