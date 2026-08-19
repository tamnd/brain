---
title: "CF 102163E - Adnan and the Burned drivers"
description: "We maintain a mutable string of lowercase letters. An update changes one position to a specified character. A query gives a range ([l,r]), and we must decide whether the substring inside that range reads identically from both directions."
date: "2026-08-19T07:46:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "E"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 151
verified: true
draft: false
---

[CF 102163E - Adnan and the Burned drivers](https://codeforces.com/problemset/problem/102163/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a mutable string of lowercase letters. An update changes one position to a specified character. A query gives a range ([l,r]), and we must decide whether the substring inside that range reads identically from both directions.

For example, if the current string is `abacaba`, the range ([2,6]) contains `bacab`, which is a palindrome. A range of length one is always a palindrome, because its forward and backward representations contain the same single character.

There can be up to (10^5) positions and (10^5) events in one test case. With that many events, checking every character in every query is too expensive. In the worst case, (10^5) queries could each inspect (10^5) characters, giving roughly (10^{10}) character comparisons. That is far beyond what a typical contest time limit permits. We need both updates and palindrome queries to be close to logarithmic time.

The first boundary case is a single-character query. For example:

```
1
1 1
a
2 1 1
```

The answer is:

```
Adnan Wins
```

A comparison routine that assumes at least two characters can accidentally reject this case.

Another easy mistake is forgetting that an update can change a character to the same character it already has. For example:

```
1
3 2
aba
1 2 b
2 1 3
```

The answer is `Adnan Wins`. The update does not change the string, so the palindrome status must remain unchanged. An implementation that treats every update as a structural change can still be correct, but it must overwrite the stored value rather than apply an incorrect incremental adjustment.

The most common boundary error appears when the queried interval touches either end of the string. For example:

```
1
5 2
abcba
2 1 5
2 2 4
```

Both answers are `Adnan Wins`. Any implementation using zero-based indexing must translate the inclusive input range carefully, because the internal representation will normally use half-open intervals.

Finally, a substring can have matching character counts and still not be a palindrome. For example, `aabb` contains two `a` characters and two `b` characters, but it is not a palindrome. A frequency-based solution would incorrectly accept it.

## Approaches

The direct solution is to inspect a queried substring from both ends. For a query ([l,r]), compare the characters at (l) and (r), then (l+1) and (r-1), continuing until the two pointers meet. This is correct because a string is a palindrome exactly when every mirrored pair contains equal characters.

The problem is the amount of work. A query on a substring of length (k) takes (O(k)) time. If the string has (10^5) characters and we perform (10^5) queries on ranges of length close to (10^5), the worst case is about (5 \times 10^9) character comparisons. Point updates do not improve this situation.

The useful observation is that a palindrome has exactly the same sequence when read forward and backward. Instead of comparing those characters one by one, we can represent the entire substring by a rolling hash. We maintain a forward hash for every segment and a reverse hash for the same segment. If the two hashes are equal, the substring is treated as a palindrome.

A segment tree is a natural fit because its nodes represent contiguous pieces of the string. Each node stores the hash of its segment from left to right and from right to left. When two adjacent segments are joined, their hashes can be combined in constant time using powers of the hashing base.

A point update affects only the (O(\log N)) segment-tree nodes on the path from the changed leaf to the root. A range query visits (O(\log N)) relevant nodes and combines their hashes in their original order. The resulting forward and reverse hashes can then be compared.

The hash comparison is probabilistic in the standard rolling-hash sense. Using two different large prime moduli makes an accidental collision extremely unlikely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N)) per query, (O(NE)) worst case | (O(N)) | Too slow |
| Segment Tree + Double Hash | (O(\log N)) per event | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Precompute powers of the hashing base modulo both chosen primes. We need (B^k) when combining a segment of length (k) with another segment, so computing these powers once avoids repeated exponentiation.
2. Build a segment tree over the current string. A leaf represents one character. For every node, store its forward hash, reverse hash, and segment length. For a leaf, both hashes are simply the numeric value assigned to its character.
3. When merging a left child (A) and a right child (C), suppose their lengths are (x) and (y). If a hash is defined as
[
H(s)=\sum_{i=0}^{|s|-1} value(s_i)B^i,
]
then the forward hash of (AC) is
[
H(A)+B^xH(C).
]
The reverse hash is formed in the same way, but the reversed left and right pieces appear in the opposite conceptual order:
[
RH(C)+B^yRH(A).
]
Both formulas take constant time.
4. For an update `1 i c`, convert (i) to the segment tree's indexing convention and replace the corresponding leaf with the value of `c`. Recompute every ancestor using the merge formulas. Only (O(\log N)) nodes change because a point belongs to one root-to-leaf path.
5. For a query `2 l r`, retrieve the aggregate node information for exactly that interval. When several pieces are returned, concatenate them in left-to-right order using the same merge operation. The query therefore produces one forward hash and one reverse hash for the complete substring.
6. Compare the two resulting hashes under both moduli. If both match, print `Adnan Wins`; otherwise print `ARCNCD!`. A palindrome has identical forward and reversed sequences, so their hashes must agree. With double hashing, a non-palindrome passing both comparisons is negligibly unlikely.

Why it works: the segment-tree invariant is that every node stores exactly the rolling hash of its represented substring and exactly the rolling hash of that substring reversed. The merge formulas preserve this invariant when two adjacent segments are combined. Point updates preserve it by rebuilding the affected path, and range queries preserve it by concatenating the selected segments in their original order. Consequently, the final forward hash represents the queried substring and the final reverse hash represents that same substring backwards. Equal hashes mean the two representations match, which is precisely the palindrome condition, up to the negligible probability of a double hash collision.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD1 = 1_000_000_007
MOD2 = 1_000_000_009
BASE = 911382323

def solve_case(n, q, s, queries):
    size = 1
    while size < n:
        size <<= 1

    # Powers used when concatenating hashes.
    pow1 = [1] * (n + 1)
    pow2 = [1] * (n + 1)

    for i in range(1, n + 1):
        pow1[i] = pow1[i - 1] * BASE % MOD1
        pow2[i] = pow2[i - 1] * BASE % MOD2

    total = size << 1

    # Forward hashes.
    hf1 = [0] * total
    hf2 = [0] * total

    # Reverse hashes.
    hr1 = [0] * total
    hr2 = [0] * total

    # Segment lengths.
    length = [0] * total

    def value(ch):
        return ord(ch) - 96

    # Leaves.
    for i, ch in enumerate(s):
        p = size + i
        v = value(ch)

        hf1[p] = v
        hf2[p] = v
        hr1[p] = v
        hr2[p] = v
        length[p] = 1

    # Padding leaves have length zero.
    for p in range(size - 1, 0, -1):
        left = p << 1
        right = left | 1

        ll = length[left]
        lr = length[right]
        length[p] = ll + lr

        hf1[p] = (hf1[left] + pow1[ll] * hf1[right]) % MOD1
        hf2[p] = (hf2[left] + pow2[ll] * hf2[right]) % MOD2

        hr1[p] = (hr1[right] + pow1[lr] * hr1[left]) % MOD1
        hr2[p] = (hr2[right] + pow2[lr] * hr2[left]) % MOD2

    def pull(p):
        left = p << 1
        right = left | 1

        ll = length[left]
        lr = length[right]
        length[p] = ll + lr

        hf1[p] = (hf1[left] + pow1[ll] * hf1[right]) % MOD1
        hf2[p] = (hf2[left] + pow2[ll] * hf2[right]) % MOD2

        hr1[p] = (hr1[right] + pow1[lr] * hr1[left]) % MOD1
        hr2[p] = (hr2[right] + pow2[lr] * hr2[left]) % MOD2

    def update(pos, ch):
        p = size + pos
        v = value(ch)

        hf1[p] = v
        hf2[p] = v
        hr1[p] = v
        hr2[p] = v
        length[p] = 1

        p >>= 1
        while p:
            pull(p)
            p >>= 1

    def merge(a, b):
        # Each item is:
        # (forward_hash_1, forward_hash_2,
        #  reverse_hash_1, reverse_hash_2, length)
        if a[4] == 0:
            return b
        if b[4] == 0:
            return a

        a1, a2, ar1, ar2, la = a
        b1, b2, br1, br2, lb = b

        return (
            (a1 + pow1[la] * b1) % MOD1,
            (a2 + pow2[la] * b2) % MOD2,
            (br1 + pow1[lb] * ar1) % MOD1,
            (br2 + pow2[lb] * ar2) % MOD2,
            la + lb
        )

    def query(left, right):
        # Convert [left, right) into segment-tree coordinates.
        left += size
        right += size

        res_left = (0, 0, 0, 0, 0)
        res_right = (0, 0, 0, 0, 0)

        while left < right:
            if left & 1:
                node = (
                    hf1[left], hf2[left],
                    hr1[left], hr2[left],
                    length[left]
                )
                res_left = merge(res_left, node)
                left += 1

            if right & 1:
                right -= 1
                node = (
                    hf1[right], hf2[right],
                    hr1[right], hr2[right],
                    length[right]
                )
                res_right = merge(node, res_right)

            left >>= 1
            right >>= 1

        return merge(res_left, res_right)

    output = []

    for typ, x, y in queries:
        if typ == 1:
            update(x - 1, y)
        else:
            # Input uses inclusive [x, y].
            # query() uses half-open [x - 1, y).
            h1, h2, rh1, rh2, _ = query(x - 1, y)

            if h1 == rh1 and h2 == rh2:
                output.append("Adnan Wins")
            else:
                output.append("ARCNCD!")

    return "\n".join(output)

def main():
    t = int(input())
    answers = []

    for _ in range(t):
        n, q = map(int, input().split())
        s = input().strip()

        queries = []
        for _ in range(q):
            parts = input().split()
            typ = int(parts[0])

            if typ == 1:
                queries.append((1, int(parts[1]), parts[2]))
            else:
                queries.append((2, int(parts[1]), int(parts[2])))

        answers.append(solve_case(n, q, s, queries))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    main()
```

The two power arrays are built first because every merge needs (B^k), where (k) is the length of one of the child segments. Since all queried lengths are at most (N), (N+1) powers are sufficient.

The segment tree uses an iterative layout with leaves beginning at `size`. The actual string occupies the first (N) leaves, while any extra leaves created because `size` is a power of two remain empty. Their length is zero, so they contribute nothing to a merge.

The `pull` function implements the segment invariant. For the forward direction, the left segment remains at its current exponents and the right segment is shifted by the left segment's length. For the reverse direction, the right segment comes first because the reverse of `left + right` is `reverse(right) + reverse(left)`.

The query routine uses two accumulators. `res_left` receives selected nodes encountered from the left and appends them normally. `res_right` receives selected nodes encountered from the right and prepends each new node. This ordering is necessary because the segment-tree traversal does not necessarily encounter all selected nodes from left to right.

The input interval is inclusive, while the internal query function uses a half-open interval. Thus an input query `[l, r]` becomes `query(l - 1, r)`. This single conversion is responsible for several otherwise easy off-by-one bugs.

Python integers do not overflow, but the hash values must remain inside the chosen modular ranges. Every multiplication and addition in the hash formulas is followed by `% MOD1` or `% MOD2`. There is no integer-overflow concern beyond the normal Python arbitrary-precision arithmetic.

The implementation stores both directions and both moduli directly in the tree. This uses more memory than storing a single hash, but it remains (O(N)) and comfortably fits the 256 MB limit for (N \le 10^5).

## Worked Examples

For the provided sample, the initial string is `adaersd`. The update at position 5 changes `r` to `a`, producing `adaeasd`. The query ([3,5]) is `aea`, which is a palindrome.

| Event | Operation | Current string | Queried substring | Forward = Reverse? | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | `1 5 a` | `adaeasd` |  |  |  |
| 2 | `2 3 5` | `adaeasd` | `aea` | Yes | `Adnan Wins` |
| 3 | `2 1 6` | `adaeasd` | `adaeas` | No | `ARCNCD!` |
| 4 | `1 1 d` | `ddaeasd` |  |  |  |
| 5 | `2 1 2` | `ddaeasd` | `dd` | Yes | `Adnan Wins` |

The trace demonstrates that the tree represents the current string after every update, not merely the original string. The final query also exercises a range starting at the first position.

A second example shows a palindrome becoming non-palindromic after a single update:

```
1
5 3
abcba
2 1 5
1 3 d
2 1 5
```

| Event | Operation | Current string | Query | Forward hash | Reverse hash | Output |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `2 1 5` | `abcba` | `[1,5]` | Equal | Equal | `Adnan Wins` |
| 2 | `1 3 d` | `abdba` |  |  |  |  |
| 3 | `2 1 5` | `abdba` | `[1,5]` | Equal | Equal | `Adnan Wins` |

This particular update happens to preserve the palindrome because `abdba` is also symmetric. To demonstrate a failed query as well, change the update to position 2:

```
1
3 2
aba
1 2 c
2 1 3
```

| Event | Operation | Current string | Query | Result |
| --- | --- | --- | --- | --- |
| 1 | `1 2 c` | `aca` |  |  |
| 2 | `2 1 3` | `aca` | `[1,3]` | `Adnan Wins` |

The invariant is visible in both traces: whenever the queried substring is symmetric, its forward and reverse representations are identical.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N + E\log N)) | Building the tree and powers takes (O(N)), while every update and query takes (O(\log N)). |
| Space | (O(N)) | The powers and all segment-tree arrays contain (O(N)) elements. |

With (N,E \le 10^5), the algorithm performs only logarithmically many tree operations per event. The total number of segment-tree levels is about 17 for (10^5) elements, so roughly (O(10^5 \log 10^5)) node operations are required rather than billions of character comparisons. The memory usage is linear and remains within the 256 MB limit.

## Test Cases

```python
# This test harness contains the same algorithm as the submission,
# exposed through run() so that the assertions can execute it.

import sys
import io

MOD1 = 1_000_000_007
MOD2 = 1_000_000_009
BASE = 911382323

def solve_case(n, q, s, queries):
    size = 1
    while size < n:
        size <<= 1

    pow1 = [1] * (n + 1)
    pow2 = [1] * (n + 1)

    for i in range(1, n + 1):
        pow1[i] = pow1[i - 1] * BASE % MOD1
        pow2[i] = pow2[i - 1] * BASE % MOD2

    total = size << 1
    hf1 = [0] * total
    hf2 = [0] * total
    hr1 = [0] * total
    hr2 = [0] * total
    length = [0] * total

    def value(ch):
        return ord(ch) - 96

    for i, ch in enumerate(s):
        p = size + i
        v = value(ch)
        hf1[p] = hf2[p] = hr1[p] = hr2[p] = v
        length[p] = 1

    def pull(p):
        left = p << 1
        right = left | 1

        ll = length[left]
        lr = length[right]
        length[p] = ll + lr

        hf1[p] = (hf1[left] + pow1[ll] * hf1[right]) % MOD1
        hf2[p] = (hf2[left] + pow2[ll] * hf2[right]) % MOD2
        hr1[p] = (hr1[right] + pow1[lr] * hr1[left]) % MOD1
        hr2[p] = (hr2[right] + pow2[lr] * hr2[left]) % MOD2

    for p in range(size - 1, 0, -1):
        pull(p)

    def update(pos, ch):
        p = size + pos
        v = value(ch)
        hf1[p] = hf2[p] = hr1[p] = hr2[p] = v
        length[p] = 1

        p >>= 1
        while p:
            pull(p)
            p >>= 1

    def merge(a, b):
        if a[4] == 0:
            return b
        if b[4] == 0:
            return a

        a1, a2, ar1, ar2, la = a
        b1, b2, br1, br2, lb = b

        return (
            (a1 + pow1[la] * b1) % MOD1,
            (a2 + pow2[la] * b2) % MOD2,
            (br1 + pow1[lb] * ar1) % MOD1,
            (br2 + pow2[lb] * ar2) % MOD2,
            la + lb
        )

    def query(left, right):
        left += size
        right += size

        a = (0, 0, 0, 0, 0)
        b = (0, 0, 0, 0, 0)

        while left < right:
            if left & 1:
                a = merge(a, (
                    hf1[left], hf2[left],
                    hr1[left], hr2[left],
                    length[left]
                ))
                left += 1

            if right & 1:
                right -= 1
                b = merge((
                    hf1[right], hf2[right],
                    hr1[right], hr2[right],
                    length[right]
                ), b)

            left >>= 1
            right >>= 1

        return merge(a, b)

    ans = []

    for typ, x, y in queries:
        if typ == 1:
            update(x - 1, y)
        else:
            h1, h2, rh1, rh2, _ = query(x - 1, y)
            if h1 == rh1 and h2 == rh2:
                ans.append("Adnan Wins")
            else:
                ans.append("ARCNCD!")

    return "\n".join(ans)

def run(inp: str) -> str:
    data = io.StringIO(inp)
    t = int(data.readline())
    all_answers = []

    for _ in range(t):
        n, q = map(int, data.readline().split())
        s = data.readline().strip()

        queries = []
        for _ in range(q):
            parts = data.readline().split()
            if parts[0] == "1":
                queries.append((1, int(parts[1]), parts[2]))
            else:
                queries.append((2, int(parts[1]), int(parts[2])))

        all_answers.append(solve_case(n, q, s, queries))

    return "\n".join(all_answers)

# Provided sample.
sample1 = """\
1
7 5
adaersd
1 5 a
2 3 5
2 1 6
1 1 d
2 1 2
"""

assert run(sample1) == """\
Adnan Wins
ARCNCD!
Adnan Wins
""".strip(), "sample 1"

# Minimum size and length-one palindrome.
case2 = """\
1
1 3
a
2 1 1
1 1 z
2 1 1
"""

assert run(case2) == """\
Adnan Wins
Adnan Wins
""".strip(), "minimum size"

# All equal characters remain palindromes after updates.
case3 = """\
1
5 4
aaaaa
2 1 5
1 3 a
2 2 4
2 1 4
"""

assert run(case3) == """\
Adnan Wins
Adnan Wins
Adnan Wins
""".strip(), "all equal"

# Boundary queries and a change that destroys the palindrome.
case4 = """\
1
5 4
abcba
2 1 5
2 2 4
1 1 z
2 1 5
"""

assert run(case4) == """\
Adnan Wins
Adnan Wins
ARCNCD!
""".strip(), "boundary and update"

# Maximum-size construction. The first query is a palindrome,
# then one endpoint changes and the full-range query must fail.
n = 100000
case5 = (
    "1\n"
    f"{n} 3\n"
    + "a" * n
    + "\n2 1 100000\n"
    + "1 1 b\n"
    + "2 1 100000\n"
)

assert run(case5) == """\
Adnan Wins
ARCNCD!
""".strip(), "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `Adnan Wins`, `ARCNCD!`, `Adnan Wins` | Official update and range-query sequence |
| `N=1`, one-character ranges | `Adnan Wins` twice | Minimum size and singleton intervals |
| `aaaaa` | Three `Adnan Wins` answers | All-equal values and unchanged updates |
| `abcba` with an endpoint update | `Adnan Wins`, `Adnan Wins`, `ARCNCD!` | Full-range boundaries and update propagation |
| `100000` equal characters | `Adnan Wins`, `ARCNCD!` | Maximum size and performance |

## Edge Cases

A singleton interval needs no special case in the tree. For the input

```
1
1 1
a
2 1 1
```

the internal interval is `[0,1)`, so the query returns a segment of length one. Its forward and reverse hashes are both the value of `a`, and the program prints `Adnan Wins`.

An update that assigns the current character again is handled by replacing the leaf with the same value and rebuilding its ancestors. For

```
1
3 2
aba
1 2 b
2 1 3
```

the string remains `aba`, so the full-range hashes remain equal and the output is `Adnan Wins`. The implementation does not assume that every update changes the value.

A query touching the right boundary exercises the conversion from inclusive to half-open indexing. For

```
1
5 2
abcba
2 1 5
2 2 4
```

the first query becomes `[0,5)` and the second becomes `[1,4)`. Their substrings are `abcba` and `bcb`, respectively, and both have matching forward and reverse hashes. Both outputs are `Adnan Wins`.

A non-palindrome with symmetric character frequencies catches approaches based only on counts. For example,

```
1
4 1
aabb
2 1 4
```

produces `ARCNCD!`. The forward sequence is `aabb`, while the reverse is `bbaa`. The segment tree stores these two different hashes, so it rejects the range even though the frequencies of `a` and `b` are identical.

The full-string update case also checks that changes propagate all the way to the root. Starting with `abcba`, changing position 1 to `z` produces `zbcba`. A query over `[1,5]` then compares `zbcba` against `abcbz`, which are different, so the answer is `ARCNCD!`. This confirms that the update path correctly rebuilds every ancestor whose stored substring contains the changed position.
