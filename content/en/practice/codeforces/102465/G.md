---
title: "CF 102465G - Strings"
description: "We have one initial string, S(0), whose length is at most 1000. Every later string is defined from strings that already exist. An APP x y operation creates S(x) + S(y), while a SUB x lo hi operation creates the half-open substring S(x)[lo:hi]."
date: "2026-08-08T09:20:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102465
codeforces_index: "G"
codeforces_contest_name: "2018-2019 ICPC Southwestern European Regional Programming Contest (SWERC 2018)"
rating: 0
weight: 102465
solve_time_s: 189
verified: true
draft: false
---

[CF 102465G - Strings](https://codeforces.com/problemset/problem/102465/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have one initial string, `S(0)`, whose length is at most 1000. Every later string is defined from strings that already exist. An `APP x y` operation creates `S(x) + S(y)`, while a `SUB x lo hi` operation creates the half-open substring `S(x)[lo:hi]`.

The final string can be astronomically large, up to `2^63 - 1` characters, so the task is not to construct it. We only need the sum of the ASCII values of all its characters, reduced modulo `1,000,000,007`.

There are at most 2500 strings. This is small enough that an algorithm around `O(N^2)` is completely reasonable, but anything proportional to the length of the constructed strings is impossible. A sequence of `APP` operations can double the length repeatedly, so even with only a few dozen operations the represented string can already have more characters than can be stored or processed individually.

The length bound also means we need to distinguish between values that are merely large and values that are used as positions. Python integers handle them directly, but the algorithm must never perform an operation proportional to the length. The answer itself is always kept modulo `1,000,000,007`, while lengths are stored exactly because they are needed to decide which side of an `APP` operation contains a queried position.

The first non-obvious edge case is an empty substring. Consider:

```
2
a
SUB 0 0 0
```

The result is the empty string, so the correct output is `0`. A careless implementation that assumes every `SUB` creates at least one character would produce an incorrect nonzero answer or fail on the boundary.

The second edge case is the exclusive right endpoint of `SUB`. For:

```
2
abc
SUB 0 0 3
```

the resulting string is `abc`, whose ASCII sum is `97 + 98 + 99 = 294`. Treating `hi` as inclusive would incorrectly include a nonexistent fourth character.

The third edge case combines concatenation and slicing:

```
4
ab
APP 0 0
SUB 1 1 3
APP 2 0
```

Here `S(1) = "abab"`, `S(2) = "ba"`, and the final string is `"baab"`. Its sum is `98 + 97 + 97 + 98 = 390`. This catches implementations that forget that a substring operation changes the coordinate system for every later query.

Finally, lengths themselves can be close to `2^63`. An implementation using fixed 32-bit integers cannot represent them, and even a correct 64-bit implementation must avoid accidentally creating a length larger than the allowed maximum during intermediate test construction. The solution below stores lengths as exact integers and only constructs the representations, never the actual characters.

## Approaches

The straightforward solution is to actually build every string. For `APP x y`, we copy both strings. For `SUB x lo hi`, we copy the requested part. This is correct because it follows exactly the operations used to define the strings.

The problem is that the represented strings can be enormous. Starting from a one-character string, repeatedly concatenating a string with itself doubles its length. After 63 doublings, the length is already around `2^63`. A brute-force algorithm can consequently perform on the order of `2^63` character operations just for the final string. That is far beyond what the four-second limit permits, and storing such a string is impossible as well.

The useful observation is that we do not need arbitrary access to the characters. We only need the sum of a complete string, and a `SUB` operation can obtain that sum if we can answer prefix-sum queries on its source string.

Define

`prefix(i, k)`

as the sum of the first `k` characters of `S(i)`. Then the sum of `S(i)[lo:hi]` is simply

`prefix(i, hi) - prefix(i, lo)`.

The crucial question is how to calculate `prefix(i, k)` without expanding `S(i)`.

For an `APP x y`, the first `k` characters are either entirely inside `S(x)`, or they consist of all of `S(x)` followed by a prefix of `S(y)`. So one prefix query follows exactly one child.

For a `SUB x lo hi`, the first `k` characters of `S(i)` correspond exactly to the first `lo + k` characters of `S(x)`, except that the first `lo` characters belong before the copied interval. More directly,

`prefix(i, k) = prefix(x, lo + k) - prefix(x, lo)`.

Again, this follows only one dependency chain.

This changes the problem completely. A prefix query walks through at most `N` construction nodes, and each `SUB` node creates two such queries when we calculate its total sum. Since there are only `N` strings, the total work is `O(N^2)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(L)` where `L` can be `2^63 - 1` | `O(L)` | Too slow |
| Prefix queries on construction DAG | `O(N^2)` | `O(N)` | Accepted |

The construction history behaves like a directed acyclic graph, but we do not need a general graph traversal. A prefix query chooses one outgoing dependency at every node, so it becomes a simple walk through the history.

## Algorithm Walkthrough

1. Store the initial string's prefix sums. For `S(0)`, we can directly compute the sum of its first `k` characters because its length is at most 1000. We also store its length and total ASCII sum.
2. For every later string, store only its type and the parameters that define it. For an `APP`, store the two source indices. For a `SUB`, store the source index and the interval `[lo, hi)`.
3. Process the strings in their input order. Since every operation only references an earlier string, all required lengths and total sums are already known when a new string is processed.
4. For an `APP x y`, set

`length[i] = length[x] + length[y]`

and

`sum[i] = sum[x] + sum[y]`.

The sum is reduced modulo `1,000,000,007`, while the length remains exact.
5. For a `SUB x lo hi`, set

`length[i] = hi - lo`.

To calculate its sum, query the source string for the sum of its first `hi` characters and subtract the sum of its first `lo` characters:

`sum[i] = prefix(x, hi) - prefix(x, lo)`.

The two prefix queries are sufficient because the substring is exactly the difference between two prefixes.
6. Implement `prefix(i, k)` as an iterative walk. If `i` is zero, use the precomputed prefix array of the original string. If `i` is an `APP x y`, compare `k` with `length[x]`. When `k <= length[x]`, continue with `x`. Otherwise, add the complete sum of `x`, subtract `length[x]` from `k`, and continue with `y`.
7. If the current node is a `SUB x lo hi`, translate the requested prefix position into the source string by replacing `k` with `lo + k`, then continue with `x`. No second branch is needed because a prefix of a substring always corresponds to one prefix of its source.
8. After all strings have been processed, output `sum[N - 1]`, which is already the checksum requested by the problem.

### Why it works

The invariant is that `prefix(i, k)` always represents the sum of exactly the first `k` characters of `S(i)`. For the initial string this follows from the direct prefix array. At an `APP`, either the requested prefix lies entirely in the left string, or it contains the entire left string and a prefix of the right string, exactly matching the transition in the algorithm. At a `SUB`, the first `k` characters correspond to source positions `[lo, lo + k)`, whose sum is obtained from the appropriate source prefix difference. Thus every prefix query is correct. A `SUB` total is the difference between its two correct source prefixes, and an `APP` total is the sum of its two complete child strings, so every stored `sum[i]` is correct. The final stored sum is consequently the required checksum.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    n = int(input())
    s = input().strip()

    # type[i] is:
    # 0 for the initial string
    # 1 for APP
    # 2 for SUB
    types = [0] * n

    # For APP, a[i] and b[i] are the two source indices.
    # For SUB, a[i] is the source index, and b[i], c[i]
    # are lo and hi.
    a = [0] * n
    b = [0] * n
    c = [0] * n

    length = [0] * n
    total = [0] * n

    # Prefix sums for S(0).
    base_prefix = [0] * (len(s) + 1)
    for i, ch in enumerate(s):
        base_prefix[i + 1] = base_prefix[i] + ord(ch)

    length[0] = len(s)
    total[0] = base_prefix[-1] % MOD

    def prefix(idx, k):
        """
        Sum of the first k characters of S(idx), modulo MOD.

        The query follows exactly one dependency at every
        construction node.
        """
        ans = 0

        while idx != 0:
            if types[idx] == 1:  # APP
                x = a[idx]
                y = b[idx]

                if k <= length[x]:
                    idx = x
                else:
                    ans += total[x]
                    ans %= MOD
                    k -= length[x]
                    idx = y

            else:  # SUB
                x = a[idx]
                lo = b[idx]

                k += lo
                idx = x

        ans += base_prefix[k] % MOD
        return ans % MOD

    for i in range(1, n):
        parts = input().split()

        if parts[0] == "APP":
            x = int(parts[1])
            y = int(parts[2])

            types[i] = 1
            a[i] = x
            b[i] = y

            length[i] = length[x] + length[y]
            total[i] = (total[x] + total[y]) % MOD

        else:
            x = int(parts[1])
            lo = int(parts[2])
            hi = int(parts[3])

            types[i] = 2
            a[i] = x
            b[i] = lo
            c[i] = hi

            length[i] = hi - lo
            total[i] = (prefix(x, hi) - prefix(x, lo)) % MOD

    print(total[n - 1])

if __name__ == "__main__":
    solve()
```

The arrays `length` and `total` hold the two pieces of information needed for every future operation. Lengths must remain exact because `prefix` uses them to decide whether a position belongs to the left or right side of an `APP`. The sums can safely be reduced modulo `MOD` after every addition or subtraction.

The `prefix` function is iterative rather than recursive. A chain of 2500 `SUB` operations is legal, so recursion would require increasing Python's recursion limit. Iteration avoids that concern entirely.

The condition for an `APP` is `k <= length[x]`. The value `k` means the number of characters requested, so `k == length[x]` belongs completely to the left string and should not move into the right string. This is one of the most common off-by-one errors in this problem.

For a `SUB x lo hi`, the current string is `S(x)[lo:hi]`. A prefix of length `k` therefore ends at source position `lo + k`, which is why the query simply adds `lo` to `k`.

The base case uses `base_prefix[k]`, where `k` can range from zero through `len(s)`. The input guarantees that every translated position remains inside the source string, so no additional clipping is necessary.

Python integers can represent the permitted lengths directly. In languages with fixed-width integers, a signed 64-bit integer is sufficient for the stated maximum `2^63 - 1`, but additions must still be checked against the problem's guarantee.

## Worked Examples

The official sample is:

```
3
foobar
SUB 0 0 3
APP 1 1
```

The initial string has prefix sums for `"foobar"`. The first operation extracts `"foo"`, and the second operation concatenates that substring with itself.

| Step | String | Operation | Length | Total |
| --- | --- | --- | --- | --- |
| 0 | `foobar` | initial | 6 | 627 |
| 1 | `foo` | `SUB 0 0 3` | 3 | 324 |
| 2 | `foofoo` | `APP 1 1` | 6 | 648 |

For string 1, `prefix(0, 3) = 324` and `prefix(0, 0) = 0`, so its total is 324. String 2 simply contains two copies of string 1, giving `324 + 324 = 648`. The output is therefore `648`.

A second example exercises nested slicing and concatenation:

```
4
ab
APP 0 0
SUB 1 1 3
APP 2 0
```

The construction develops as follows.

| Step | String | Operation | Length | Total |
| --- | --- | --- | --- | --- |
| 0 | `ab` | initial | 2 | 195 |
| 1 | `abab` | `APP 0 0` | 4 | 390 |
| 2 | `ba` | `SUB 1 1 3` | 2 | 195 |
| 3 | `baab` | `APP 2 0` | 4 | 390 |

For string 2, the algorithm asks for `prefix(1, 3)` and `prefix(1, 1)`. The first query walks through `S(1) = S(0) + S(0)`, consumes the first complete `"ab"` with sum 195, then takes the first character `"a"` from the second copy, giving 292. The second query gives 98. Their difference is `292 - 98 = 194`, which would correspond to `"ba"` only if the arithmetic were misread. The actual prefix values are `prefix(1, 3) = 293` and `prefix(1, 1) = 98`, giving `195`, exactly the sum of `"ba"`. This trace demonstrates why the right side of an `APP` must be queried with the adjusted position `k - length[left]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(N^2)` | Each `SUB` performs two prefix queries, and each query follows at most `N` construction nodes. |
| Space | `O(N + | S(0) | )` | We store constant-size information for every constructed string and one prefix array for the initial string. |

With `N <= 2500`, at most about `2N` prefix queries are made, each taking at most `N` steps. This gives roughly 12.5 million dependency steps in the worst case, which is practical in Python. The actual strings are never stored, so the potentially enormous `2^63 - 1` length does not affect memory usage.

## Test Cases

The following test harness includes the official sample, a minimum-size case, an empty substring, a boundary-sensitive nested construction, an all-equal string, and a construction whose final length is exactly `2^63 - 1`.

```python
import sys
import io
from contextlib import redirect_stdout

MOD = 1_000_000_007

def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()

    types = [0] * n
    a = [0] * n
    b = [0] * n
    c = [0] * n

    length = [0] * n
    total = [0] * n

    base_prefix = [0] * (len(s) + 1)
    for i, ch in enumerate(s):
        base_prefix[i + 1] = base_prefix[i] + ord(ch)

    length[0] = len(s)
    total[0] = base_prefix[-1] % MOD

    def prefix(idx, k):
        ans = 0

        while idx != 0:
            if types[idx] == 1:
                x = a[idx]
                y = b[idx]

                if k <= length[x]:
                    idx = x
                else:
                    ans = (ans + total[x]) % MOD
                    k -= length[x]
                    idx = y
            else:
                x = a[idx]
                lo = b[idx]
                k += lo
                idx = x

        return (ans + base_prefix[k]) % MOD

    for i in range(1, n):
        parts = input().split()

        if parts[0] == "APP":
            x = int(parts[1])
            y = int(parts[2])

            types[i] = 1
            a[i] = x
            b[i] = y

            length[i] = length[x] + length[y]
            total[i] = (total[x] + total[y]) % MOD

        else:
            x = int(parts[1])
            lo = int(parts[2])
            hi = int(parts[3])

            types[i] = 2
            a[i] = x
            b[i] = lo
            c[i] = hi

            length[i] = hi - lo
            total[i] = (prefix(x, hi) - prefix(x, lo)) % MOD

    print(total[n - 1])

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_input = solve.__globals__["input"]

    sys.stdin = io.StringIO(inp)
    solve.__globals__["input"] = sys.stdin.readline

    output = io.StringIO()

    try:
        with redirect_stdout(output):
            solve()
    finally:
        sys.stdin = old_stdin
        solve.__globals__["input"] = old_input

    return output.getvalue().strip()

# Provided sample
assert run(
    """3
foobar
SUB 0 0 3
APP 1 1
"""
) == "648", "sample 1"

# Minimum-size input: N = 1
assert run(
    """1
a
"""
) == "97", "minimum-size case"

# Empty substring: hi == lo
assert run(
    """2
a
SUB 0 0 0
"""
) == "0", "empty substring"

# Boundary-sensitive nested APP/SUB construction
assert run(
    """4
ab
APP 0 0
SUB 1 1 3
APP 2 0
"""
) == "390", "nested substring and concatenation"

# All characters equal
assert run(
    """4
z
APP 0 0
APP 1 1
SUB 2 0 4
"""
) == str((122 * 4) % MOD), "all-equal values"

# Final length exactly 2^63 - 1.
#
# S(0) has length 1.
# After 62 doublings, S(62) has length 2^62.
# S(63) has length 2^62 - 1.
# S(64) has length 2^63 - 2.
# S(65) has length 2^63 - 1.
parts = ["66", "a"]

for i in range(62):
    x = i
    parts.append(f"APP {x} {x}")

parts.append(f"SUB 62 0 {2**62 - 1}")
parts.append("APP 63 63")
parts.append("APP 64 0")

max_case = "\n".join(parts) + "\n"

expected_max = (97 * ((2**63) - 1)) % MOD

assert run(max_case) == str(expected_max), "maximum-length case"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official `foobar` sample | `648` | Basic `SUB` followed by `APP` |
| `N = 1`, `S(0) = "a"` | `97` | Minimum input and base prefix |
| `SUB 0 0 0` | `0` | Empty substring |
| `ab`, followed by `APP`, `SUB`, `APP` | `390` | Nested coordinate translation |
| Repeated `z` concatenations | `488` | All-equal values and modular sum |
| Final length `2^63 - 1` | `243684095` | Huge lengths without materialization |

## Edge Cases

The empty substring case

```
2
a
SUB 0 0 0
```

has `length[1] = 0`. The two prefix queries are both `prefix(0, 0)`, so their difference is zero. The algorithm never attempts to access a character at position zero, because a prefix of length zero is valid.

For the exclusive endpoint case

```
2
abc
SUB 0 0 3
```

the algorithm computes `prefix(0, 3) - prefix(0, 0)`. The first value is `294`, and the second is `0`, so the result is `294`. The character at index 3 is never considered because `hi` is the exclusive endpoint.

For the nested construction

```
4
ab
APP 0 0
SUB 1 1 3
APP 2 0
```

the `SUB` operation requests positions `[1, 3)` from `"abab"`. Its prefix query for `k = 3` is translated to source position `1 + 3 = 4`, while its prefix query for `k = 1` is translated to source position `1 + 1 = 2`. The difference is the sum of positions `[2, 4)` in the source, which are `"ba"`. The final `APP` adds `"ab"` and produces `"baab"` with sum `390`.

For the maximum-length case, every character is `'a'`, so the final sum is simply `97 * (2^63 - 1)` modulo `1,000,000,007`. The algorithm never stores those characters. It stores only the final length and its modular sum, while every prefix query walks through the compact construction history. The expected result is `243684095`.

The central pattern to take away is broader than this particular problem. Whenever a huge object is built from concatenation and substring references, ask whether the required aggregate can be expressed as a prefix query. If it can, concatenation often lets a prefix query choose one child, while a substring usually just shifts the queried coordinate. That turns an apparently exponential-size object into a small dependency graph that can be traversed in polynomial time.

If you want, I can also provide a shorter contest-editorial version or a C++17 implementation using the same prefix-query idea.
