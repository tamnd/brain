---
title: "CF 102881G - Baby Ehab and a GCD Problem, Of Course"
description: "We have an initially empty collection of numbered cubes. Each operation adds every cube whose number lies in a given inclusive interval [l, r]. After each operation, we need to print the greatest common divisor of all numbers that have appeared in the collection so far."
date: "2026-07-25T12:40:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102881
codeforces_index: "G"
codeforces_contest_name: "ECPC 2019 Kickoff"
rating: 0
weight: 102881
solve_time_s: 40
verified: true
draft: false
---

[CF 102881G - Baby Ehab and a GCD Problem, Of Course](https://codeforces.com/problemset/problem/102881/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an initially empty collection of numbered cubes. Each operation adds every cube whose number lies in a given inclusive interval `[l, r]`. After each operation, we need to print the greatest common divisor of all numbers that have appeared in the collection so far.

The input is a sequence of interval additions. The important detail is that the collection only grows, so each answer depends on all previous intervals as well as the current one. The output after every operation is the current global GCD.

The number of operations can reach `10^5`, and the values inside intervals can be as large as `10^18`. This immediately rules out iterating over the numbers inside an interval. A single interval may contain up to `10^18` numbers, so even handling one large query by visiting every value is impossible. We need a constant-time or logarithmic-time update per query.

The key edge cases come from intervals that look large but are mathematically simple. A single-value interval and a multi-value interval behave completely differently. For example, with input:

```
1
2250 2250
```

the answer is:

```
2250
```

because the only cube added has value `2250`.

Another case is:

```
2
10 10
15 15
```

The answers are:

```
10
5
```

The second answer is not `15`, because the current cubes are `10` and `15`, whose GCD is `5`.

The most important boundary case is an interval with two consecutive values:

```
1
7 8
```

The answer is:

```
1
```

A careless solution might try to compute the GCD using only the endpoints and get `gcd(7, 8) = 1`, which happens to work here, but the reason is deeper: every interval containing consecutive integers has GCD `1`. This property is what allows us to avoid processing the interval.

## Approaches

A direct approach would maintain all numbers that have been added and compute the GCD over the entire collection after every query. This is correct because the GCD of a set is exactly the value requested by the problem. However, it fails immediately on the constraints. An interval such as `[1, 10^18]` contains a quintillion numbers, so even storing the values is impossible, and recomputing the GCD after each operation could require up to `10^23` operations over all queries.

The observation that changes the problem is that we never need to know the individual numbers inside an interval. We only need the GCD contributed by that interval.

For any interval containing at least two numbers, there are two consecutive integers inside it. The GCD of two consecutive integers is always `1`, and adding more numbers cannot increase the GCD. Therefore every interval `[l, r]` where `l < r` contributes a GCD of `1`.

If the interval contains only one number, its contribution is simply that number.

The whole problem reduces to maintaining the GCD of the previous answer and the contribution of the new interval. Once the answer becomes `1`, it can never change again because every future GCD with `1` remains `1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total number of inserted values) | O(total number of inserted values) | Too slow |
| Optimal | O(q log A) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize the current GCD as `0`. The GCD of `0` and a value `x` is `x`, which lets the first update work naturally.
2. For every interval `[l, r]`, determine what GCD this interval adds. If `l` and `r` are different, the interval contains consecutive numbers, so its contribution is `1`. Otherwise, its contribution is `l`.
3. Combine the new contribution with the current answer using the GCD operation. The updated value is the GCD of every number seen so far.
4. Output the updated GCD.

Why it works: the invariant maintained after every query is that `current_gcd` equals the GCD of every cube that has appeared up to that point. When a new interval is added, the GCD of all numbers in that interval is either its single value or `1`. Taking the GCD of the old collection and this new interval gives exactly the GCD of the combined collection, so the invariant remains true.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def solve():
    q = int(input())
    ans = 0
    out = []

    for _ in range(q):
        l, r = map(int, input().split())

        if l != r:
            add = 1
        else:
            add = l

        ans = gcd(ans, add)
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The variable `ans` stores the GCD of every cube processed so far. Starting it at `0` avoids needing a special case for the first query because `gcd(0, x)` returns `x`.

For each interval, the code checks whether it contains more than one number. The condition `l != r` is enough because the interval is inclusive, so any different endpoints mean there are at least two consecutive integers inside.

The update uses Python's built-in Euclidean algorithm implementation through `math.gcd`, which handles values up to `10^18` efficiently. No array or interval storage is needed because past information is fully summarized by one integer.

## Worked Examples

### Sample 1

Input:

```
4
2250 2250
126 126
1 6
6 8
```

| Step | Interval | Interval GCD | Current GCD |
| --- | --- | --- | --- |
| 1 | [2250, 2250] | 2250 | 2250 |
| 2 | [126, 126] | 126 | 18 |
| 3 | [1, 6] | 1 | 1 |
| 4 | [6, 8] | 1 | 1 |

The first two operations only add individual numbers, so the answer changes according to the GCD of those values. The third operation contains consecutive numbers, forcing the answer to become `1`. After that, later intervals cannot change it.

### Sample 2

Input:

```
3
8 8
20 20
30 30
```

| Step | Interval | Interval GCD | Current GCD |
| --- | --- | --- | --- |
| 1 | [8, 8] | 8 | 8 |
| 2 | [20, 20] | 20 | 4 |
| 3 | [30, 30] | 30 | 2 |

This trace demonstrates that single-number intervals are handled exactly like inserting one more value into the current GCD.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log A) | Each query performs one GCD operation on numbers up to `10^18`. |
| Space | O(1) | Only the current GCD and output storage are maintained. |

With `q` up to `10^5`, this approach performs only a small number of arithmetic operations per query and easily fits the limits.

## Test Cases

```python
import sys
import io
from math import gcd

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    q = int(sys.stdin.readline())
    ans = 0
    out = []

    for _ in range(q):
        l, r = map(int, sys.stdin.readline().split())
        if l != r:
            ans = gcd(ans, 1)
        else:
            ans = gcd(ans, l)
        out.append(str(ans))

    print("\n".join(out))

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result.strip()

assert run("""4
2250 2250
126 126
1 6
6 8
""") == """2250
18
1
1""", "sample 1"

assert run("""3
8 8
20 20
30 30
""") == """8
4
2""", "sample 2"

assert run("""1
1 1
""") == "1", "minimum value"

assert run("""3
1000000000000000000 1000000000000000000
1000000000000000000 1000000000000000000
1 1000000000000000000
""") == """1000000000000000000
1000000000000000000
1""", "large values and interval collapse"

assert run("""4
42 42
42 42
42 42
42 42
""") == """42
42
42
42""", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single value `[1,1]` | `1` | Handles the smallest possible interval. |
| Large single values followed by a large interval | `1` at the end | Confirms that huge ranges are not iterated over. |
| Repeated `[42,42]` intervals | Always `42` | Checks repeated identical contributions. |
| Sample intervals | Matches sample output | Confirms the main transition from normal GCD updates to the permanent `1` state. |

## Edge Cases

For the single-value case:

```
1
2250 2250
```

the algorithm sees `l == r`, so the interval contributes `2250`. The previous GCD is `0`, making the new answer `gcd(0, 2250) = 2250`.

For multiple individual values:

```
2
10 10
15 15
```

the first update gives `10`. The second contributes `15`, so the answer becomes `gcd(10, 15) = 5`. The algorithm never needs to store either cube because the current GCD contains all required information.

For an interval containing consecutive values:

```
1
7 8
```

the interval contributes `1` because it contains both `7` and `8`, and `gcd(7, 8) = 1`. The global answer becomes `1`. Any future operation will keep the answer at `1`, because no integer has a GCD larger than `1` when combined with an existing GCD of `1`.
