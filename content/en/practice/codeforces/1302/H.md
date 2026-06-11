---
title: "CF 1302H - Who needs suffix structures?"
description: "We are given a sequence of length n. Although the statement talks about a string, the characters are represented by integers, and the alphabet is extremely large. The large alphabet size means we cannot rely on tricks that depend on a small number of distinct symbols."
date: "2026-06-11T18:13:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 1302
codeforces_index: "H"
codeforces_contest_name: "AIM Tech Poorly Prepared Contest (unrated, funny, Div. 1 preferred)"
rating: 0
weight: 1302
solve_time_s: 112
verified: true
draft: false
---

[CF 1302H - Who needs suffix structures?](https://codeforces.com/problemset/problem/1302/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of length `n`. Although the statement talks about a string, the characters are represented by integers, and the alphabet is extremely large. The large alphabet size means we cannot rely on tricks that depend on a small number of distinct symbols.

Each query specifies two starting positions and a length. We must determine whether the two contiguous segments of that length are identical.

More concretely, for a query `(len, pos1, pos2)`, we compare:

- `a[pos1 ... pos1 + len - 1]`
- `a[pos2 ... pos2 + len - 1]`

and print `"Yes"` if every corresponding element matches, otherwise `"No"`.

The constraints are the key part of the problem. Both `n` and `q` can reach 200,000. A direct comparison of two substrings takes `O(len)` time. In the worst case, `len` is also 200,000, so a single query may require 200,000 comparisons. With 200,000 queries, that becomes roughly `4 × 10^10` element comparisons, which is far beyond what can be executed within a 2-second limit.

The task is really a large number of substring equality checks on a static sequence. That structure strongly suggests building a preprocessing data structure that can answer each query in constant or logarithmic time.

Several edge cases deserve attention.

Consider identical starting positions:

```
n = 5
a = [1,2,3,4,5]

query: len=5, pos1=1, pos2=1
```

The answer is obviously `"Yes"`. Any correct substring comparison method must handle this without special cases.

Consider comparisons that reach the very end of the array:

```
n = 5
a = [1,2,3,4,5]

query: len=2, pos1=4, pos2=4
```

The compared segment is `[4,5]`. Off-by-one mistakes in prefix computations often appear here.

Another important case is when two substrings share a long common prefix but differ at the end:

```
a = [7,7,7,7,8]
query: len=5, pos1=1, pos2=?
```

A careless optimization that only checks a partial prefix could incorrectly conclude equality. The entire length must be verified through a collision-resistant representation.

Finally, the alphabet contains values up to 987,898,788. Any approach that assumes characters fit into a small alphabet, such as fixed-size frequency arrays or transition tables indexed by character value, is inappropriate.

## Approaches

The brute-force solution is straightforward. For each query, compare the two requested substrings element by element. If all positions match, output `"Yes"`; otherwise output `"No"`.

The brute-force method is correct because substring equality is defined exactly by equality at every position. The problem is its running time. A query may require `O(len)` work, and `len` may be `O(n)`. With `q = 200000` and `n = 200000`, the worst case becomes `O(nq)`, approximately forty billion comparisons.

The array never changes, and every query asks the same kind of question: are two ranges equal? Instead of repeatedly inspecting the underlying elements, we can preprocess the sequence and assign a compact fingerprint to every prefix. Then the fingerprint of any substring can be extracted in constant time.

Polynomial rolling hash is a natural fit. Let

$$H[i]$$

denote the hash of the first `i` elements. Using powers of a fixed base, the hash of any substring can be recovered from two prefix hashes.

If two substrings are equal, their hashes are equal. With double hashing, the probability of different substrings producing the same pair of hashes becomes negligible. After preprocessing, each query reduces to comparing two hash pairs, which takes constant time.

The brute-force solution repeatedly examines the same elements. Hashing compresses each substring into a constant-size representation, allowing each query to be answered immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) worst case | O(1) | Too slow |
| Optimal (double rolling hash) | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the sequence.
2. Choose two large moduli and a fixed base.
3. Precompute powers of the base modulo both moduli.

These powers allow us to normalize substring hashes in constant time.
4. Build prefix hash arrays for both moduli.

For each position, extend the previous prefix hash by appending the current value.
5. Define a function `get_hash(l, r)` that returns the hash pair of the subarray from `l` to `r` inclusive.

Using prefix hashes:

$$H(l,r)=H[r]-H[l-1]\cdot P^{r-l+1}$$

computed modulo each modulus.
6. For every query, convert the 1-based positions into the corresponding interval endpoints.
7. Compute the hash pair of the first substring.
8. Compute the hash pair of the second substring.
9. If both hash pairs are identical, print `"Yes"`, otherwise print `"No"`.

### Why it works

The prefix hash construction guarantees that every substring is represented by a polynomial expression over its elements. Removing the contribution of the prefix before the substring yields a value depending only on the substring itself.

Two equal substrings generate exactly the same polynomial and therefore exactly the same hash pair. Each query compares the hash representations of the two requested ranges. Since both hashes are extracted using the same formula, equal substrings always compare equal. Double hashing makes accidental collisions negligibly unlikely, which is the standard competitive programming guarantee used for substring equality queries.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    MOD1 = 1_000_000_007
    MOD2 = 1_000_000_009
    BASE = 911382323

    pow1 = [1] * (n + 1)
    pow2 = [1] * (n + 1)

    for i in range(1, n + 1):
        pow1[i] = (pow1[i - 1] * BASE) % MOD1
        pow2[i] = (pow2[i - 1] * BASE) % MOD2

    pref1 = [0] * (n + 1)
    pref2 = [0] * (n + 1)

    for i in range(n):
        pref1[i + 1] = (pref1[i] * BASE + a[i] + 1) % MOD1
        pref2[i + 1] = (pref2[i] * BASE + a[i] + 1) % MOD2

    def get_hash(l, r):
        h1 = (
            pref1[r]
            - pref1[l - 1] * pow1[r - l + 1]
        ) % MOD1

        h2 = (
            pref2[r]
            - pref2[l - 1] * pow2[r - l + 1]
        ) % MOD2

        return h1, h2

    ans = []

    for _ in range(q):
        length, p1, p2 = map(int, input().split())

        h_first = get_hash(p1, p1 + length - 1)
        h_second = get_hash(p2, p2 + length - 1)

        ans.append("Yes" if h_first == h_second else "No")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The preprocessing stage builds powers of the base and prefix hashes. Both arrays are indexed from zero, while substring queries are naturally expressed using 1-based positions, so the hash extraction formula is written directly in 1-based form.

Adding `1` to each element before inserting it into the hash prevents zero values from becoming invisible in leading positions. Without this adjustment, some polynomial representations become less robust.

The `get_hash` function is the critical piece. It removes the contribution of everything before position `l` and leaves only the polynomial corresponding to the requested interval. The length of the interval determines which power multiplier must be removed.

Each query computes two hash pairs and compares them. No traversal of the underlying substring is required.

## Worked Examples

### Sample 1

Input:

```
5 2
1 2 3 1 2
2 1 4
3 1 3
```

The substrings involved are:

| Query | First substring | Second substring | Result |
| --- | --- | --- | --- |
| (2,1,4) | [1,2] | [1,2] | Yes |
| (3,1,3) | [1,2,3] | [3,1,2] | No |

Hash comparison behaves as follows:

| Query | Range 1 | Range 2 | Hashes equal? | Output |
| --- | --- | --- | --- | --- |
| 1 | [1,2] | [4,5] | Yes | Yes |
| 2 | [1,3] | [3,5] | No | No |

This example demonstrates the main idea: equality testing becomes hash comparison rather than element comparison.

### Custom Example

Input:

```
6 3
5 5 5 5 5 5
1 1 6
3 1 4
6 1 1
```

All substrings consist entirely of the value `5`.

| Query | Range 1 | Range 2 | Hashes equal? | Output |
| --- | --- | --- | --- | --- |
| 1 | [1,1] | [6,6] | Yes | Yes |
| 2 | [1,3] | [4,6] | Yes | Yes |
| 3 | [1,6] | [1,6] | Yes | Yes |

This example shows that repeated values do not create difficulties. Equal ranges always generate identical hashes regardless of where they occur.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | O(n) preprocessing and O(1) work per query |
| Space | O(n) | Prefix hashes and power tables |

With `n, q ≤ 200000`, linear preprocessing and constant-time queries are easily fast enough. The memory usage is also comfortably within the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    MOD1 = 1_000_000_007
    MOD2 = 1_000_000_009
    BASE = 911382323

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    pow1 = [1] * (n + 1)
    pow2 = [1] * (n + 1)

    for i in range(1, n + 1):
        pow1[i] = (pow1[i - 1] * BASE) % MOD1
        pow2[i] = (pow2[i - 1] * BASE) % MOD2

    pref1 = [0] * (n + 1)
    pref2 = [0] * (n + 1)

    for i in range(n):
        pref1[i + 1] = (pref1[i] * BASE + a[i] + 1) % MOD1
        pref2[i + 1] = (pref2[i] * BASE + a[i] + 1) % MOD2

    def get_hash(l, r):
        return (
            (pref1[r] - pref1[l - 1] * pow1[r - l + 1]) % MOD1,
            (pref2[r] - pref2[l - 1] * pow2[r - l + 1]) % MOD2,
        )

    ans = []

    for _ in range(q):
        length, p1, p2 = map(int, input().split())
        ans.append(
            "Yes"
            if get_hash(p1, p1 + length - 1)
            == get_hash(p2, p2 + length - 1)
            else "No"
        )

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return "\n".join(ans) + ("\n" if ans else "")

# provided sample
assert run(
"""5 2
1 2 3 1 2
2 1 4
3 1 3
"""
) == "Yes\nNo\n", "sample 1"

# minimum size
assert run(
"""1 1
7
1 1 1
"""
) == "Yes\n"

# all equal
assert run(
"""5 2
4 4 4 4 4
3 1 3
2 2 4
"""
) == "Yes\nYes\n"

# boundary at end of array
assert run(
"""5 1
1 2 3 4 5
2 4 4
"""
) == "Yes\n"

# off-by-one check
assert run(
"""5 1
1 2 3 4 5
2 1 2
"""
) == "No\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | Yes | Smallest legal input |
| All values equal | Yes, Yes | Repeated-pattern handling |
| Query ending at position n | Yes | Boundary correctness |
| Adjacent unequal substrings | No | Off-by-one protection |

## Edge Cases

Consider the smallest possible instance:

```
1 1
7
1 1 1
```

The only substring is `[7]`. The hash of range `[1,1]` is computed twice and compared with itself. Both hashes match, so the answer is `"Yes"`.

Consider a query touching the end of the array:

```
5 1
1 2 3 4 5
2 4 4
```

The compared ranges are `[4,5]` and `[4,5]`. The hash function extracts exactly two elements because the length used in the power term is `r - l + 1 = 2`. No extra element is included, and no element is omitted.

Consider two ranges with a long common prefix:

```
5 1
7 7 7 7 8
4 1 2
```

The compared substrings are:

```
[7,7,7,7]
[7,7,7,8]
```

The first three positions match, but the last differs. Their polynomial hashes differ because the final coefficient contributes a different value. The algorithm outputs `"No"`.

Consider identical starting positions:

```
5 1
1 2 3 4 5
5 1 1
```

Both queried intervals are exactly the same range. The extracted hash pair is identical, and the algorithm returns `"Yes"` immediately through the normal comparison logic. No special handling is required.
