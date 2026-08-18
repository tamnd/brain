---
title: "CF 102180B - \u041f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \u0433\u0430\u0440\u0434\u0435\u0440\u043e\u0431\u0430"
description: "Katya examines (n) T-shirts in a fixed order. Each T-shirt has a model identifier (ai). When she sees an identifier for the first time, she buys that T-shirt. Every later T-shirt with the same identifier is skipped."
date: "2026-08-19T06:45:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102180
codeforces_index: "B"
codeforces_contest_name: "MSPU Training Contest 2018-2019"
rating: 0
weight: 102180
solve_time_s: 69
verified: true
draft: false
---

[CF 102180B - \u041f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \u0433\u0430\u0440\u0434\u0435\u0440\u043e\u0431\u0430](https://codeforces.com/problemset/problem/102180/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

Katya examines (n) T-shirts in a fixed order. Each T-shirt has a model identifier (a_i). When she sees an identifier for the first time, she buys that T-shirt. Every later T-shirt with the same identifier is skipped. The task is to produce an array of (n) binary values, where position (i) contains (1) exactly when the T-shirt at position (i) is the first occurrence of its identifier.

The input contains the number of T-shirts and then their identifiers in viewing order. The identifiers can be as large as (10^9), so they cannot be treated as small array indices without additional assumptions. The number of T-shirts is at most (5000), which is small enough for a quadratic solution to be feasible in some languages, but the intended solution is linear and is just as simple.

A straightforward implementation can compare each identifier with every earlier identifier. With (n=5000), that can require roughly (n(n-1)/2 = 12{,}497{,}500) comparisons in the worst case. That amount is not enormous, but it is unnecessary, and a hash set gives a direct constant-average-time membership test.

The first edge case is a sequence containing only one T-shirt. For input `1` followed by `7`, the answer is `1`, because there is no earlier occurrence to match it. An implementation that initializes every answer to zero and only marks values after detecting a duplicate would incorrectly produce zero.

Another edge case is repeated identifiers immediately next to each other. For input `4` with identifiers `9 9 9 9`, the correct output is `1 0 0 0`. The first `9` is purchased, and every subsequent `9` has already been encountered. A careless implementation that compares only with the previous element would happen to work here, but that reasoning is insufficient for non-consecutive duplicates.

For example, with input `5` and identifiers `1 2 1 3 2`, the correct output is `1 1 0 1 0`. The third element repeats the first one, while the fifth repeats the second one. An approach that only checks the immediately preceding identifier would incorrectly mark the third and fifth positions as new.

The identifier value itself also needs care. An input such as `3` with identifiers `1 1000000000 1` produces `1 1 0`. The value (10^9) is perfectly valid, but it should be stored as an ordinary integer and not used as an index into a huge array.

## Approaches

The direct brute-force solution follows the definition literally. For each T-shirt, scan all positions before it and check whether its identifier has already appeared. If no equal identifier is found, output `1`; otherwise output `0`. This is correct because an identifier is new precisely when there is no equal identifier at an earlier position.

The problem with this approach is repeated searching. For the last T-shirt, we may inspect all (n-1) previous positions, for the previous one up to (n-2), and so on. In the worst case the total number of comparisons is

[
0+1+2+\dots+(n-1)=\frac{n(n-1)}2.
]

For (n=5000), this is (12{,}497{,}500) comparisons. It can still be acceptable under a generous implementation and time limit, but it is quadratic and does not scale with the same robustness as the intended method.

The key observation is that the only information we need from the past is which identifiers have already appeared. We do not care where the previous occurrence was or how many times it occurred. A set represents exactly this information. When processing (a_i), membership in the set answers the question "have we seen this model before?" in constant average time. If the answer is no, we output `1` and immediately insert the identifier into the set. If the answer is yes, we output `0`.

The brute-force method works because it searches the entire processed prefix to reconstruct the set of identifiers seen so far. The observation that this set is the only relevant part of the prefix lets us maintain it explicitly and replace an entire scan with one hash-table lookup.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(1)) extra | Accepted for these constraints, but unnecessarily slow |
| Optimal | (O(n)) average | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Create an empty set called `seen`. It will contain every model identifier encountered before the current position.
2. Create an empty result array. We will append exactly one value for each T-shirt, preserving the original order.
3. Process the identifiers from left to right. For the current identifier `x`, first check whether `x` is already in `seen`. The set represents exactly the identifiers Katya has encountered earlier, so this membership test directly answers whether she should buy the current T-shirt.
4. If `x` is not in `seen`, append `1` to the result and insert `x` into the set. The insertion must happen immediately because any later occurrence of the same model must be recognized as a duplicate.
5. If `x` is already in `seen`, append `0` to the result and leave the set unchanged. Seeing the same model again does not introduce any new information.
6. After all (n) identifiers have been processed, print the result separated by spaces.

### Why it works

After processing any prefix of the input, the invariant is that `seen` contains exactly the distinct identifiers occurring in that prefix. Initially the prefix is empty, so the invariant holds. When a new identifier is processed, it is absent from `seen`, so the algorithm outputs `1` and inserts it, preserving the invariant. When a repeated identifier is processed, it is already present, so the algorithm outputs `0` and leaves the set unchanged, also preserving the invariant.

Consequently, at every position the algorithm outputs `1` exactly when the current identifier has not occurred earlier. That is exactly the required purchase rule.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    seen = set()
    answer = []

    for x in a:
        if x in seen:
            answer.append(0)
        else:
            answer.append(1)
            seen.add(x)

    print(*answer)

if __name__ == "__main__":
    solve()
```

The first two lines of `solve` read the number of T-shirts and the complete identifier sequence. Since the statement guarantees that the second line contains all (n) identifiers, a single `split()` is sufficient.

The `seen` set corresponds directly to step 1 of the walkthrough. During the loop, membership is checked before insertion. This order matters. If the code inserted `x` before checking membership, every identifier would appear to have been seen already and every answer would become `0`.

The first occurrence enters the `else` branch, receives answer `1`, and is added to `seen`. Later occurrences enter the `if` branch and receive `0`. There is no index arithmetic in the algorithm, so there is no off-by-one boundary to manage.

Python integers handle values up to (10^9) directly, so the maximum identifier requires no special treatment. The set stores at most (n) distinct integers, and the output contains exactly (n) values.

The problem has only one test case, so there is no outer test-case loop. `sys.stdin.readline` is used as requested, while `print(*answer)` produces the required space-separated output.

## Worked Examples

### Sample 1

Input identifiers are `1 2 3`. Every identifier is new when it appears.

| Position | Current `x` | `x in seen` | Action | `seen` after step | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | No | Buy and insert 1 | `{1}` | 1 |
| 2 | 2 | No | Buy and insert 2 | `{1, 2}` | 1 |
| 3 | 3 | No | Buy and insert 3 | `{1, 2, 3}` | 1 |

The resulting output is `1 1 1`. This trace demonstrates the initial state and the case where every T-shirt has a distinct model.

### Sample 2

Input identifiers are `1 2 1 2 3`. The third and fourth T-shirts repeat models already encountered.

| Position | Current `x` | `x in seen` | Action | `seen` after step | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | No | Buy and insert 1 | `{1}` | 1 |
| 2 | 2 | No | Buy and insert 2 | `{1, 2}` | 1 |
| 3 | 1 | Yes | Skip | `{1, 2}` | 0 |
| 4 | 2 | Yes | Skip | `{1, 2}` | 0 |
| 5 | 3 | No | Buy and insert 3 | `{1, 2, 3}` | 1 |

The resulting output is `1 1 0 0 1`. The trace demonstrates why the set must remember all previous identifiers, rather than only the immediately preceding one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) average | Each identifier is checked and, for a first occurrence, inserted into a hash set |
| Space | (O(n)) | The set can contain up to (n) distinct identifiers, and the output also contains (n) values |

With (n\le 5000), the linear solution performs only a few thousand hash-table operations. The memory usage is also small compared with the 256 MB limit. The identifier bound of (10^9) does not affect the complexity because Python stores each identifier as an integer value rather than allocating an array indexed by that value.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    seen = set()
    answer = []

    for x in a:
        if x in seen:
            answer.append(0)
        else:
            answer.append(1)
            seen.add(x)

    print(*answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run("3\n1 2 3\n") == "1 1 1", "sample 1"

# Provided sample 2
assert run("5\n1 2 1 2 3\n") == "1 1 0 0 1", "sample 2"

# Provided sample 3
assert run("4\n9 9 9 9\n") == "1 0 0 0", "sample 3"

# Minimum-size input
assert run("1\n42\n") == "1", "single T-shirt"

# Maximum-size input, all identifiers distinct
n = 5000
maximum_distinct = list(range(1, n + 1))
expected = " ".join(["1"] * n)
assert run(f"{n}\n{' '.join(map(str, maximum_distinct))}\n") == expected, \
    "maximum-size distinct input"

# Maximum identifier value and non-consecutive duplicates
assert run("6\n1000000000 1 2 1000000000 2 1\n") == "1 1 1 0 0 0", \
    "identifier boundary"

# Duplicates separated by other identifiers
assert run("7\n5 8 5 9 8 10 5\n") == "1 1 0 1 0 1 0", \
    "non-consecutive duplicates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 42` | `1` | Minimum-size input and first-occurrence handling |
| `5000 / 1 2 ... 5000` | 5000 ones | Maximum (n) and all identifiers distinct |
| `6 / 1000000000 1 2 1000000000 2 1` | `1 1 1 0 0 0` | Maximum identifier value and repeated models |
| `7 / 5 8 5 9 8 10 5` | `1 1 0 1 0 1 0` | Duplicates separated by several other identifiers |

## Edge Cases

### A single T-shirt

For input

```
1
7
```

the set starts empty. The only identifier, `7`, is not in the set, so the algorithm appends `1` and inserts `7`. The final output is

```
1
```

There is no previous T-shirt, so the first occurrence must always be purchased.

### All identifiers equal

For input

```
4
9 9 9 9
```

the first `9` is absent from `seen`, so the algorithm outputs `1` and inserts it. Each of the next three `9`s is already in the set, so they each produce `0`. The final output is

```
1 0 0 0
```

The set never needs to contain multiple copies of the same identifier. This is exactly why a set is a natural representation of the relevant history.

### Repetition that is not adjacent

For input

```
5
1 2 1 3 2
```

the set evolves as `{1}`, `{1, 2}`, `{1, 2}`, `{1, 2, 3}`, `{1, 2, 3}`. The corresponding output is

```
1 1 0 1 0
```

The third position is rejected because `1` appeared at position 1, even though position 2 contained a different identifier. The fifth position is rejected because `2` appeared at position 2. This is the case that exposes an incorrect strategy based only on comparing neighboring elements.

### Maximum identifier

For input

```
3
1 1000000000 1
```

the first two identifiers are new, so they produce `1 1`. The final `1` is already in the set and produces `0`. The output is

```
1 1 0
```

The value `1000000000` requires no special handling. It is stored as an ordinary integer in the set, and its magnitude has no effect on the algorithm's running time.
