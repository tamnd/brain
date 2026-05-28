---
title: "CF 39A - C*++ Calculations"
description: "We are given an arithmetic expression built from terms involving a single variable a. Every term is one of two forms:"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "expression-parsing", "greedy"]
categories: ["algorithms"]
codeforces_contest: 39
codeforces_index: "A"
codeforces_contest_name: "School Team Contest 1 (Winter Computer School 2010/11)"
rating: 2000
weight: 39
solve_time_s: 162
verified: true
draft: false
---
[CF 39A - C*++ Calculations](https://codeforces.com/problemset/problem/39/A)

**Rating:** 2000  
**Tags:** expression parsing, greedy  
**Solve time:** 2m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an arithmetic expression built from terms involving a single variable `a`. Every term is one of two forms:

```
k * a++
k * ++a
```

where `k` is an integer coefficient between `0` and `1000`. If the coefficient is missing, it is treated as `1`.

The whole expression is a sum and subtraction of such terms. The unusual part is evaluation order. The language allows the terms to be evaluated in any order before combining them with `+` and `-`.

Each term changes the value of `a`.

For `a++`, the current value of `a` is used first, then `a` increases by `1`.

For `++a`, `a` increases first, then the new value is used.

The task is to choose the evaluation order that maximizes the final value of the whole expression.

The number of summands is at most `1000`, so any algorithm much slower than quadratic is unnecessary. Trying every permutation is impossible because `1000!` is astronomically large. Even for only `15` terms, brute force already becomes infeasible.

The expression itself is small enough that parsing it directly with a linear scan is straightforward. We only need to extract, for every summand:

```
sign: +1 or -1
coefficient: k
type: post-increment or pre-increment
```

Several edge cases are easy to mishandle.

Consider:

```
0
a++-++a
```

If we evaluate `a++` first:

```
0 - 2 = -2
```

If we evaluate `++a` first:

```
1 - 1 = 0
```

The maximum is `0`. A naive approach that only counts total increments without considering order loses this distinction.

Another subtle case is coefficient `0`.

Input:

```
5
0*a++-0*++a
```

Both terms contribute `0` numerically, but they still modify `a`. The first term increases after reading `a`, the second increases before reading it. The order still matters even though coefficients are zero.

A third trap is forgetting that subtraction flips priorities.

Input:

```
1
10*a++-1*++a
```

To maximize the result, the large positive coefficient should see a large value of `a`, while the negative term should see a small value. Evaluating the negative term first is better.

A careless greedy that only sorts by coefficient magnitude without considering sign gives the wrong result.

## Approaches

The brute-force idea is direct. Parse all summands, generate every possible evaluation order, simulate the expression, and keep the maximum result.

For each permutation, we maintain the current value of `a`. When evaluating a term:

For `k * a++`, we add `k * a` to the result, then increment `a`.

For `k * ++a`, we increment `a` first, then add `k * a`.

After all terms are evaluated, we combine them with their original `+` and `-` signs.

This works because the language semantics are exactly described by sequential evaluation. The problem is the number of permutations. With `n` summands, we need `n!` orders. Even `12!` is already about `4.8 * 10^8`, far beyond the limit.

The key observation is that every term increases `a` exactly once. The only question is which terms should receive smaller values of `a`, and which should receive larger ones.

Let us rewrite each term carefully.

Suppose current `a = x`.

For a positive term:

```
+k * a++  =>  +k * x
+k * ++a  =>  +k * (x + 1)
```

For a negative term:

```
-k * a++  =>  -k * x
-k * ++a  =>  -k * (x + 1)
```

Every term depends linearly on the current value of `a`.

If a term has larger effective coefficient on `x`, we want it evaluated later when `a` becomes larger. If it has smaller coefficient, we want it earlier.

This becomes a classic pairwise swap argument.

Take two terms with effective coefficients `c1` and `c2`.

If we evaluate term 1 before term 2:

```
c1 * x + c2 * (x + 1)
```

If we swap them:

```
c2 * x + c1 * (x + 1)
```

The second order is better exactly when:

```
c1 > c2
```

So terms should be processed in nondecreasing order of effective coefficient.

Now we only need to determine the effective coefficient for each summand.

For:

```
+k * something
```

effective coefficient is `+k`.

For:

```
-k * something
```

effective coefficient is `-k`.

The `++a` versus `a++` distinction contributes only a constant offset. Specifically, `++a` adds one extra copy of its signed coefficient because it increments before reading.

After sorting, we simulate evaluation in that order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the expression into individual summands.

For every summand, extract:

- its sign, `+1` or `-1`
- its coefficient `k`
- whether it is `a++` or `++a`
2. For each summand, compute its effective coefficient.

A positive term contributes `+k * current_a`.

A negative term contributes `-k * current_a`.

Store:

```
effective = sign * k
```
3. Sort all summands by `effective` in nondecreasing order.

Smaller coefficients should consume smaller values of `a`. Larger coefficients should consume larger values of `a`.
4. Simulate the evaluation in sorted order.

Maintain:

- current value of `a`
- accumulated answer
5. When processing `a++`:

Add:

```
sign * k * a
```

then increment `a`.
6. When processing `++a`:

Increment `a` first, then add:

```
sign * k * a
```
7. Output the final accumulated value.

### Why it works

Every term increases `a` exactly once, so after evaluating `t` terms, the current value of `a` is fixed regardless of order.

The only freedom is deciding which term receives which stage of `a`.

Consider two neighboring terms with effective coefficients `c1` and `c2`.

If current `a = x`, evaluating them as `(1,2)` gives:

```
c1*x + c2*(x+1)
```

Swapping them gives:

```
c2*x + c1*(x+1)
```

The second expression is larger exactly when `c1 > c2`.

So any inversion where a larger coefficient appears earlier can be improved by swapping. Repeating this argument transforms any optimal ordering into sorted order.

That proves the greedy order is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a = int(input())
    s = input().strip()

    terms = []

    i = 0
    sign = 1

    while i < len(s):
        if s[i] == '+':
            sign = 1
            i += 1
        elif s[i] == '-':
            sign = -1
            i += 1

        coeff = 0
        has_coeff = False

        while i < len(s) and s[i].isdigit():
            coeff = coeff * 10 + int(s[i])
            has_coeff = True
            i += 1

        if has_coeff:
            i += 1  # skip '*'
        else:
            coeff = 1

        if s[i:i + 3] == "++a":
            typ = 1
            i += 3
        else:
            typ = 0
            i += 3

        effective = sign * coeff
        terms.append((effective, sign, coeff, typ))

    terms.sort(key=lambda x: x[0])

    ans = 0
    cur = a

    for _, sign, coeff, typ in terms:
        if typ == 1:
            cur += 1
            ans += sign * coeff * cur
        else:
            ans += sign * coeff * cur
            cur += 1

    print(ans)

solve()
```

The parser scans the expression from left to right. Each iteration extracts exactly one summand.

The coefficient parsing needs special care because coefficients may be omitted. If no digits are found, the coefficient must become `1`.

The distinction between `++a` and `a++` is represented with `typ`.

```
typ = 1  -> ++a
typ = 0  -> a++
```

The sorting key is only the effective coefficient:

```
sign * coeff
```

That is the quantity controlling whether a term prefers earlier or later values of `a`.

During simulation, the increment order matters. For `++a`, increment happens before contribution. For `a++`, contribution happens before increment. Mixing these two cases is the most common implementation bug.

Python integers automatically handle all possible values safely, so overflow is not a concern.

## Worked Examples

### Example 1

Input:

```
1
5*a++-3*++a+a++
```

Parsed terms:

| Term | Effective |

|---|---|---|

| `5*a++` | `5` |

| `-3*++a` | `-3` |

| `a++` | `1` |

Sorted order:

```
-3*++a
a++
5*a++
```

Simulation:

| Step | Term | a before | Contribution | a after | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | `-3*++a` | 1 | `-3 * 2 = -6` | 2 | -6 |
| 2 | `a++` | 2 | `2` | 3 | -4 |
| 3 | `5*a++` | 3 | `15` | 4 | 11 |

Final answer:

```
11
```

This example demonstrates the main greedy idea. The negative coefficient is evaluated first so it receives the smallest possible value of `a`.

### Example 2

Input:

```
3
a+++a++
```

Parsed terms:

| Term | Effective |
| --- | --- |
| `a++` | `1` |
| `a++` | `1` |

Any order is equivalent.

Simulation:

| Step | Term | a before | Contribution | a after | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | `a++` | 3 | 3 | 4 | 3 |
| 2 | `a++` | 4 | 4 | 5 | 7 |

Final answer:

```
7
```

This confirms that equal coefficients can appear in any order without changing the result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting the summands dominates |
| Space | O(n) | storing parsed terms |

With at most `1000` summands, `O(n log n)` is easily fast enough. The memory usage is tiny because we only store a few integers per term.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        a = int(input())
        s = input().strip()

        terms = []

        i = 0
        sign = 1

        while i < len(s):
            if s[i] == '+':
                sign = 1
                i += 1
            elif s[i] == '-':
                sign = -1
                i += 1

            coeff = 0
            has_coeff = False

            while i < len(s) and s[i].isdigit():
                coeff = coeff * 10 + int(s[i])
                has_coeff = True
                i += 1

            if has_coeff:
                i += 1
            else:
                coeff = 1

            if s[i:i + 3] == "++a":
                typ = 1
                i += 3
            else:
                typ = 0
                i += 3

            effective = sign * coeff
            terms.append((effective, sign, coeff, typ))

        terms.sort(key=lambda x: x[0])

        ans = 0
        cur = a

        for _, sign, coeff, typ in terms:
            if typ == 1:
                cur += 1
                ans += sign * coeff * cur
            else:
                ans += sign * coeff * cur
                cur += 1

        print(ans)

    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = old_stdout
    return out.getvalue()

# provided sample
assert run("1\n5*a++-3*++a+a++\n") == "11\n", "sample 1"

# minimum size
assert run("0\na++\n") == "0\n", "single term"

# ordering with negative coefficient
assert run("0\na++-++a\n") == "0\n", "negative term should go first"

# zero coefficients still increment
assert run("5\n0*a++-0*++a\n") == "0\n", "zero coefficient behavior"

# equal coefficients
assert run("3\na+++a++\n") == "7\n", "equal priorities"

# larger coefficients later
assert run("1\n10*a++-1*a++\n") == "19\n", "sorting correctness"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0\na++` | `0` | single summand parsing |
| `0\na++-++a` | `0` | negative terms should be early |
| `5\n0*a++-0*++a` | `0` | zero coefficients still modify `a` |
| `3\na+++a++` | `7` | equal effective coefficients |
| `1\n10*a++-1*a++` | `19` | greedy sorting order |

## Edge Cases

Consider:

```
0
a++-++a
```

The parsed effective coefficients are:

```
1
-1
```

Sorted order:

```
-++a
a++
```

Simulation:

| Step | Term | a before | Contribution | a after | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | `-++a` | 0 | -1 | 1 | -1 |
| 2 | `a++` | 1 | 1 | 2 | 0 |

Final answer:

```
0
```

The algorithm correctly places the negative coefficient first so it receives the smallest possible value of `a`.

Now consider zero coefficients:

```
5
0*a++-0*++a
```

Even though both numerical contributions are zero, both terms still increment `a`.

Sorted effective coefficients:

```
0
0
```

Simulation:

| Step | Term | a before | Contribution | a after | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | `0*a++` | 5 | 0 | 6 | 0 |
| 2 | `-0*++a` | 6 | 0 | 7 | 0 |

Final answer remains `0`.

This case confirms that the implementation handles side effects independently from arithmetic contribution.

Finally, consider:

```
1
10*a++-1*a++
```

Effective coefficients:

```
10
-1
```

Sorted order:

```
-1*a++
10*a++
```

Simulation:

| Step | Term | a before | Contribution | a after | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | `-1*a++` | 1 | -1 | 2 | -1 |
| 2 | `10*a++` | 2 | 20 | 3 | 19 |

Output:

```
19
```

A naive left-to-right evaluation gives only:

```
10 - 2 = 8
```

This example demonstrates why reordering is essential.
