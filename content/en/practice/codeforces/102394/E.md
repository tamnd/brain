---
title: "CF 102394E - Exchanging Gifts"
description: "We start with a very long array of gift types. Position (i) initially contains (gi). We may arbitrarily exchange gifts between contestants, so the final array can be any permutation of the original multiset of gift types."
date: "2026-08-10T19:06:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102394
codeforces_index: "E"
codeforces_contest_name: "The 2019 China Collegiate Programming Contest Harbin Site"
rating: 0
weight: 102394
solve_time_s: 96
verified: true
draft: false
---

[CF 102394E - Exchanging Gifts](https://codeforces.com/problemset/problem/102394/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a very long array of gift types. Position (i) initially contains (g_i). We may arbitrarily exchange gifts between contestants, so the final array can be any permutation of the original multiset of gift types.

A contestant is happy when the value placed at their position after the exchanges differs from the value they originally had. The task is to maximize the number of such positions.

The difficulty is that the final array (g=s_n) is not given explicitly. A sequence can either be written directly, with up to (10^6) values, or be formed by concatenating two previously defined sequences. A sequence may be reused many times, so its actual length can reach (10^{18}). The input itself is much smaller than the sequence it describes.

The first simplification is to ignore the order of the array. Suppose the most frequent gift type occurs (M) times and the whole array has length (L). If (M\le L/2), we can arrange the gifts so that every position receives a different type, giving (L) happy contestants. If (M>L/2), there are (M) positions originally holding that dominant type, but only (L-M) gifts of other types available to move into them. At least (M-(L-M)=2M-L) of those positions must keep the same type. All other positions can be made different. Thus the answer is

[
\min(L,2(L-M)).
]

Equivalently,

[
\text{answer}=
\begin{cases}
L,&2M\le L,\
2(L-M),&2M>L.
\end{cases}
]

So the entire problem has been reduced to finding two quantities for (s_n): its length (L), and the largest frequency (M) of any gift type.

The constraints make expanding (s_n) impossible. The number of sequence definitions is at most (10^6), and the total number of explicitly listed values over all test cases is also at most (10^6), but a generated sequence can have length (10^{18}). Even a linear scan of the expanded array could require (10^{18}) operations. A quadratic approach is ruled out much earlier, since even (10^6) input objects already makes (10^{12}) operations infeasible. The intended algorithm must work on the compressed description and spend time proportional to the input size.

There are several edge cases where a direct implementation can silently fail.

For a single element, the contestant cannot receive a different gift. For example,

```
1
1
1 1 7
```

has answer (0). A formula that assumes there are always enough other gifts to move around would incorrectly claim that the contestant can become happy.

All gifts being identical is another extreme. For

```
1
1
1 4 5 5 5 5
```

the answer is (0). Every permutation is identical to the original array. A solution that only checks whether the array contains more than one distinct value is not enough, because the important quantity is the maximum frequency.

The exact half-frequency boundary also matters. For

```
1
1
1 4 1 1 2 2
```

each value occurs twice, so every position can receive the other value and the answer is (4). Using a strict comparison with (L/2) in the wrong direction can incorrectly leave some contestant unhappy.

Finally, repeated sequence references must be counted with their multiplicity. Consider

```
1
3
1 1 1
2 1 1
2 2 2
```

The final sequence has (4) copies of (1), despite only one explicit occurrence appearing in the input. Its answer is (0). An implementation that processes each sequence definition only once without recording how many times it is referenced by the final sequence will get this wrong.

## Approaches

The brute-force approach is straightforward. First expand every concatenation until the complete array (g) is available. Then count the occurrences of every gift type, find the maximum frequency (M), and use the formula above to calculate the maximum number of happy contestants.

This is correct because exchanging gifts never changes the multiset of values. Once we know the frequency of every value, the original construction of the array no longer matters.

The problem is the size of the expanded array. A chain such as

```
1 1 7
2 1 1
2 2 2
2 3 3
...
```

can double the length at every step. After only 60 concatenations, the length can already be (2^{60}), which is larger than (10^{18}). Expanding such an array would require about (10^{18}) element operations, even though the input contains only a few dozen lines.

The key observation is that concatenation only adds frequencies. If a sequence (s_i) is used once inside the final sequence, every element of (s_i) contributes once. If it is used three times, every element of (s_i) contributes three times.

This gives a useful interpretation of the sequence definitions as a directed acyclic graph. A type-2 sequence (s_i=s_x+s_y) has edges to (s_x) and (s_y). Starting from (s_n), we can propagate a multiplicity backwards. Let (w_i) be the number of times the entire sequence (s_i) occurs in the expanded (s_n). Initially (w_n=1). Whenever (s_i=s_x+s_y), every occurrence of (s_i) creates one occurrence of both (s_x) and (s_y), so

[
w_x\mathrel{+}=w_i,\qquad
w_y\mathrel{+}=w_i.
]

Because every referenced sequence has a smaller index, processing indices from (n) down to (1) is enough.

When we reach a directly specified sequence containing values (q_1,\ldots,q_k), every one of those explicit values appears (w_i) times in the final sequence. We can add (w_i) to the global frequency of each value. The total length can be accumulated at the same time as (w_i\cdot k).

This turns the impossible task of traversing up to (10^{18}) elements into a traversal of only the explicitly supplied elements and sequence definitions. This is the same reverse marking principle used in the reference solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(L+n)), (L\le 10^{18}) | (O(L)) | Too slow |
| Optimal | (O(n+\sum k)) expected | (O(n+\sum k)) | Accepted |

## Algorithm Walkthrough

1. Read all sequence definitions. For a directly specified sequence, store its values. For a concatenation, store the two referenced sequence indices. We keep the definitions because the actual sequences may be astronomically large.
2. Create an array (w) of multiplicities and set (w_n=1). This means that the final sequence currently contains one copy of (s_n).
3. Process sequence indices from (n) down to (1). If (w_i=0), the sequence (s_i) does not contribute to the final answer, so it can be skipped.
4. If (s_i) is a concatenation (s_x+s_y), add (w_i) to both (w_x) and (w_y). Each occurrence of (s_i) contains exactly one occurrence of each child sequence.
5. If (s_i) is an explicitly listed sequence with (k) values, add (w_i) to the frequency of every listed value. Also add (w_i k) to the total length. Since the sequence is processed only when its multiplicity has already been determined, every explicit occurrence is counted with exactly the number of times it appears in (s_n).
6. Track the largest global frequency (M) while accumulating the values. There is no need to reconstruct the final array.
7. After all relevant leaves have been processed, let (L) be the total length. If (2M\le L), answer (L). Otherwise answer (2(L-M)). The first case means every position can receive a different type. In the second case, the dominant value has too many copies, so exactly (2M-L) positions are forced to keep it.

### Why it works

The invariant is that immediately before processing sequence (s_i), (w_i) equals the number of times (s_i) occurs in the fully expanded final sequence (s_n). It is true initially because (s_n) occurs once. For a concatenation (s_i=s_x+s_y), every occurrence of (s_i) contributes one occurrence of each child, so adding (w_i) to both children preserves the invariant. At a leaf, multiplying every explicitly listed value by (w_i) therefore contributes exactly its true number of occurrences in the final sequence.

After all leaves have been processed, (L) and every gift frequency are exact. The minimum number of unchanged positions is (0) when the largest frequency is at most half the array, and otherwise it is (2M-L), because only (L-M) non-dominant gifts exist to occupy the (M) dominant positions. Hence the computed answer is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    out = []

    for _ in range(T):
        n = int(input())

        kind = bytearray(n + 1)
        left = [0] * (n + 1)
        right = [0] * (n + 1)
        leaves = [None] * (n + 1)

        for i in range(1, n + 1):
            parts = list(map(int, input().split()))

            if parts[0] == 1:
                kind[i] = 1
                k = parts[1]
                leaves[i] = parts[2:]
            else:
                left[i] = parts[1]
                right[i] = parts[2]

        # ways[i] = number of times sequence i occurs in s_n.
        ways = [0] * (n + 1)
        ways[n] = 1

        freq = {}
        total = 0
        maximum = 0

        for i in range(n, 0, -1):
            w = ways[i]
            if w == 0:
                continue

            if kind[i] == 1:
                values = leaves[i]
                total += w * len(values)

                for v in values:
                    nv = freq.get(v, 0) + w
                    freq[v] = nv
                    if nv > maximum:
                        maximum = nv

                # Release the large list as soon as it is no longer needed.
                leaves[i] = None
            else:
                x = left[i]
                y = right[i]
                ways[x] += w
                ways[y] += w

        if maximum * 2 <= total:
            answer = total
        else:
            answer = 2 * (total - maximum)

        out.append(str(answer))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `kind`, `left`, and `right` arrays store the compressed DAG. `leaves[i]` is populated only for directly specified sequences, so no generated sequence is ever materialized.

The `ways` array implements the reverse propagation from the final sequence. The order from (n) down to (1) is valid because every concatenation refers only to earlier sequences. A child therefore receives all of its contributions before the algorithm reaches that child.

The dictionary `freq` stores the frequency of each actual gift type. The dictionary is necessary because gift values can be as large as (10^9) and are not suitable for direct indexing. The frequency itself can be as large as (10^{18}), so Python integers are useful here. In C++, these quantities need 64-bit integers. The official constraints explicitly allow sequence lengths up to (10^{18}).

The expression `maximum * 2 <= total` handles the exact half boundary correctly. When the maximum frequency is exactly half of the total, every position can still be changed.

The list for a leaf is released after processing it. This does not change the asymptotic memory usage, but it reduces peak memory pressure during the reverse traversal.

## Worked Examples

### Sample 1

The first sample consists of one explicitly given sequence:

```
[3, 3, 2, 1, 3]
```

The reverse traversal has only one node.

| Sequence | Multiplicity | Leaf values | Total length | Maximum frequency |
| --- | --- | --- | --- | --- |
| (s_1) | 1 | 3, 3, 2, 1, 3 | 5 | 3 |

The gift type (3) occurs three times. Since (2M=6>5), one position is forced to keep type (3), while the other four positions can receive a different type. The answer is

[
2(5-3)=4.
]

This demonstrates the dominant-frequency case.

### Sample 2

The definitions are

```
s1 = [3, 3, 2]
s2 = [2, 2, 3, 3]
s3 = s1 + s2
```

We start with (w_3=1).

| Sequence processed | Multiplicity | Action | Total length | Maximum frequency |
| --- | --- | --- | --- | --- |
| (s_3) | 1 | Add 1 to (w_1,w_2) | 0 | 0 |
| (s_2) | 1 | Add one 2 and two 3s | 4 | 2 |
| (s_1) | 1 | Add two 3s and one 2 | 7 | 4 |

The final frequencies are (3\mapsto4) and (2\mapsto3). Thus (L=7) and (M=4). Since (2M=8>7),

[
\text{answer}=2(7-4)=6.
]

The trace demonstrates that the concatenation itself never needs to be constructed. Only its multiplicity is propagated to its children.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+\sum k)) expected | Every sequence definition is processed once, and every explicitly listed value is counted once. Dictionary operations are expected (O(1)). |
| Space | (O(n+\sum k)) | The compressed sequence graph, leaf values, multiplicities, and frequency dictionary are stored. |

Across all test cases, both (n) and the total number of explicitly listed values are bounded by (10^6). The algorithm consequently performs only linear work in the actual input size, even when the represented sequence has length close to (10^{18}). The 512 MB memory limit is also sufficient for this representation.

## Test Cases

The test harness below assumes the submitted solution is saved as `solution.py` and exposes the `solve()` function shown above.

```python
import sys
import io

from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    """1
1
1 5 3 3 2 1 3
"""
) == "4", "sample 1"

# Provided sample 2
assert run(
    """1
3
1 3 3 3 2
1 4 2 2 3 3
2 1 2
"""
) == "6", "sample 2"

# Minimum-size case
assert run(
    """1
1
1 1 42
"""
) == "0", "single element"

# All values are equal
assert run(
    """1
1
1 5 7 7 7 7 7
"""
) == "0", "all equal"

# Exactly half of each value
assert run(
    """1
1
1 4 1 1 2 2
"""
) == "4", "exact half boundary"

# Dominant value
assert run(
    """1
1
1 4 1 1 1 2
"""
) == "2", "dominant frequency"

# Reused sequence
assert run(
    """1
3
1 1 1
2 1 1
2 2 2
"""
) == "0", "repeated references"

# Large represented length, but tiny input.
# s_61 represents 2^60 copies of 1.
huge_lines = ["1", "61", "1 1 1"]
for i in range(2, 62):
    huge_lines.append(f"2 {i - 1} {i - 1}")

huge_input = "\n".join(huge_lines) + "\n"

assert run(huge_input) == "0", "huge implicit sequence"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1 1 42` | 0 | Minimum sequence size |
| `1 / 1 / 1 5 7 7 7 7 7` | 0 | All values identical |
| `1 / 1 / 1 4 1 1 2 2` | 4 | Exact (M=L/2) boundary |
| `1 / 1 / 1 4 1 1 1 2` | 2 | Dominant-frequency formula |
| `3 / 1 1 1 / 2 1 1 / 2 2 2` | 0 | Reusing a sequence multiple times |
| 61-node doubling chain | 0 | Length far beyond explicit input size and 64-bit-scale counts |

## Edge Cases

The one-element case has (L=1) and (M=1). The algorithm processes the single leaf with multiplicity (1), obtains `total = 1` and `maximum = 1`, and enters the dominant branch because (2M>L). The answer becomes (2(1-1)=0), which matches the fact that there is no other gift available.

For the all-equal input

```
1
1
1 4 5 5 5 5
```

the only frequency is (M=4), while (L=4). The algorithm computes (2M=8>4), so the answer is (2(4-4)=0). No exchange can change any contestant's gift type.

For the exact-half input

```
1
1
1 4 1 1 2 2
```

the frequencies are (2) and (2), so (L=4) and (M=2). The condition (2M\le L) is true, giving answer (4). A valid arrangement is `[2, 2, 1, 1]`, which differs from `[1, 1, 2, 2]` at every position.

For the dominant case

```
1
1
1 4 1 1 1 2
```

the type (1) occurs three times and type (2) once. Only one non-(1) gift exists, so at most one of the three original (1)-positions can change. The other two must remain (1), giving exactly two happy contestants. The algorithm obtains (L=4), (M=3), and returns (2(4-3)=2).

For repeated references,

```
1
3
1 1 1
2 1 1
2 2 2
```

the reverse traversal starts with (w_3=1). Processing (s_3) gives (w_2=2). Processing (s_2) then gives (w_1=4). The explicit leaf `[1]` is consequently counted four times, so (L=M=4) and the answer is (0). This is precisely why propagating multiplicities rather than simply visiting each sequence once is necessary.

The final edge case is an enormous implicit sequence. A doubling chain can represent (2^{60}) copies of one value using only 61 definitions. The algorithm never attempts to create those copies. It propagates the multiplicity backward, eventually reaching the single-element leaf with a weight of (2^{60}). Python's arbitrary-precision integers represent that count exactly, and since every element has the same value, the final answer is still (0).
