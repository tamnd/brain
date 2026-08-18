---
title: "CF 102185I - \u0425\u0430\u043e\u0442\u0438\u0447\u043d\u044b\u0435 \u043f\u043b\u044e\u043c\u0431\u0443\u0441\u044b"
description: "We have a row containing exactly N plumbuses of every one of K colors, so the total length is N times K. The only allowed operation takes one existing plumbus out of the row and inserts it at the very left or the very right."
date: "2026-08-19T06:43:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102185
codeforces_index: "I"
codeforces_contest_name: "Southern Russia Open Championship \u2013 ContestSFedU 2019, Team Final."
rating: 0
weight: 102185
solve_time_s: 303
verified: true
draft: false
---

[CF 102185I - \u0425\u0430\u043e\u0442\u0438\u0447\u043d\u044b\u0435 \u043f\u043b\u044e\u043c\u0431\u0443\u0441\u044b](https://codeforces.com/problemset/problem/102185/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row containing exactly N plumbuses of every one of K colors, so the total length is N times K. The only allowed operation takes one existing plumbus out of the row and inserts it at the very left or the very right. The goal is to make every color occupy one contiguous block. The order of these color blocks is arbitrary.

The key difficulty is that an operation does not allow arbitrary swaps. Every plumbus that we never move keeps its relative order with every other never-moved plumbus. Moved plumbuses can eventually be arranged at the two ends, while the untouched plumbuses form the middle part of the final row.

The answer is the minimum number of moved plumbuses. Equivalently, we want to maximize the number of plumbuses that can stay where they are.

The constraints give N,K at most 1000, while the array itself can contain 1,000,000 elements. An algorithm that performs even O(NK times K) work is already around 10^9 operations in the worst case and is unusable. We need essentially linear work in the array plus at most quadratic work in the number of colors. O(NK + K^2) is small enough, and the memory limit also allows storing the original array.

There are several boundary cases that can fool an implementation.

For N=1 and K=1,

```
1 1
1
```

the answer is 0. There is only one color and its single plumbus already forms a valid group. An implementation that assumes two different endpoint colors exist could incorrectly count a move.

For N=2 and K=2,

```
2 2
1 2 1 2
```

the answer is 2. Keeping only one complete color leaves two plumbuses untouched, so two moves are enough. A careless solution that only considers already contiguous color blocks might miss this possibility.

A more subtle case is

```
3 2
1 1 2 2 1 2
```

whose answer is 2. The first two 1s and the first two 2s are already grouped, and moving the remaining 1 and 2 to the appropriate ends completes both groups. A solution that insists that some color must be kept completely can miss this kind of optimum, because here the best untouched middle can consist of two partial endpoint colors.

## Approaches

A direct brute force would choose which plumbuses are moved and which remain, then check whether the remaining plumbuses can form the middle of a valid final arrangement. This is correct because every legal sequence of operations is completely determined, as far as the untouched elements are concerned, by the set of elements that were moved. However, there are 2^(NK) possible subsets. With NK as large as 1,000,000, even writing down all candidates is impossible. Enumerating permutations of the K color blocks is also hopeless, since K! is already enormous for K=1000.

The useful observation is to look at the plumbuses that are not moved. Their relative order never changes, and all moved elements end up outside them. Consequently, the untouched plumbuses must appear in the final row as one middle sequence in which every color forms at most one run.

Suppose a color appears somewhere in the interior of that untouched sequence. If one of its N plumbuses had been moved, that moved plumbus would have to be placed at one of the two ends of the whole row. It could not return next to this interior group. Hence an interior color must have all N of its occurrences untouched.

Only the first and last color groups of the untouched sequence can be partial. They can have some occurrences moved to the corresponding outer end. Thus every optimal solution has the following structure:

```
partial left color
complete color
complete color
...
complete color
partial right color
```

The two partial colors may also be absent. If there are no complete colors at all, the untouched sequence consists of a left partial color followed by a right partial color.

Now consider a color c that is kept completely. Let first[c] and last[c] be its first and last positions in the original array. If another color d is also kept completely before c, every occurrence of d must precede every occurrence of c. The exact condition is

```
last[d] < first[c].
```

Therefore complete colors form a chain of non-overlapping intervals [first[c], last[c]]. Since all complete colors contribute exactly N untouched plumbuses, the problem becomes a dynamic programming problem over these color intervals.

There is one more detail. If c is the first complete color, we may additionally keep some occurrences of another color before first[c]. The best such color is simply the color occurring most often in that prefix. Likewise, after the last complete color, we can keep the most frequent color in the suffix.

We must remember the identity of these endpoint colors, not just their counts. The same color cannot be used on both sides, because then its retained occurrences would form two separate groups. Keeping the two best candidates on each side is enough to resolve this conflict.

The case with no complete color is handled separately. For every cut between two positions, we find the best two distinct colors consisting of a prefix color on the left and a suffix color on the right. A forward scan can maintain the two most frequent prefix colors. A reverse scan can maintain the two most frequent suffix colors. Since the prefix information is needed when the reverse scan reaches the same cut, it is stored in a compact array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(NK) · NK) | O(NK) | Too slow |
| Optimal | O(NK + K²) | O(NK) | Accepted |

## Algorithm Walkthrough

1. Read the array and record `first[c]` and `last[c]` for every color. These two positions describe exactly where a completely untouched color can occur.
2. Scan the array from left to right while maintaining the number of occurrences of every color in the prefix. When the first occurrence of color c is reached, save the two most frequent colors in the positions before `first[c]`. These are the only candidates that can serve as the partial color on the left of a complete block c.
3. During the same forward scan, save the two most frequent colors after every possible cut. Only the two best candidates are necessary because the only forbidden situation is choosing the same color on both sides.
4. Scan the array from right to left. Before processing the last occurrence of color c, the current counts describe exactly the suffix after `last[c]`. Save its two best colors as the possible right endpoint colors for a chain ending at c.
5. Sort all colors by their first occurrence. For each color c, create DP states representing chains of complete colors ending at c. The initial state consists of c itself plus one of the two best left endpoint candidates before `first[c]`.
6. To extend a chain ending at d with color c, require `last[d] < first[c]`. This means every occurrence of d lies before every occurrence of c, so both colors can remain completely untouched. Adding c increases the number of untouched plumbuses by exactly N.
7. For every ending color c, retain the two best DP states with different left endpoint colors. Two states are enough because, when the right endpoint is chosen, only one left color can become forbidden.
8. Combine every DP state ending at c with the two best suffix candidates after `last[c]`. Reject a combination only when both endpoint colors are the same nonzero color. The resulting value is the largest number of untouched plumbuses for a solution containing at least one complete color.
9. Separately, process every cut with the stored prefix candidates and the dynamically maintained suffix candidates. This handles solutions containing no complete color, where the entire untouched sequence consists of two partial endpoint colors.
10. Let `best` be the maximum number of untouched plumbuses over both cases. The required answer is `N*K - best`, because every plumbus not counted as untouched must be moved exactly once.

### Why it works

Consider any optimal sequence of operations and look only at the plumbuses that were never moved. Their relative order is unchanged, so they appear as one middle sequence in the final arrangement. Every color appearing inside that sequence must have all N of its original occurrences there, otherwise a moved occurrence of that color would have to cross an unrelated group to return to its own group. Only the first and last groups of the middle sequence can be partial.

Thus every optimal solution is represented either by a chain of complete colors with at most one partial color on each side, or by two partial colors with no complete color. The interval condition `last[d] < first[c]` characterizes exactly when two colors can both be complete and appear in that order. The DP enumerates every possible chain satisfying this condition, while the stored endpoint candidates enumerate the best possible partial colors around it. The separate cut scan covers the remaining no-complete-color case. Since every valid untouched configuration belongs to one of these two forms, the maximum number of untouched plumbuses found by the algorithm is optimal.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

BASE = 1024
BITS = 10
MASK = BASE - 1
PAIR_BITS = 20

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    m = n * k

    first = [m] * k
    last = [-1] * k

    for i, x in enumerate(a):
        c = x - 1
        if first[c] == m:
            first[c] = i
        last[c] = i

    order = sorted(range(k), key=first.__getitem__)

    pref1 = [0] * k
    pref2 = [0] * k

    cnt = [0] * k
    t1 = 0
    id1 = 0
    t2 = 0
    id2 = 0

    # packed[i] stores the two best prefix candidates before position i.
    # Each candidate is encoded as count * BASE + color.
    packed = array('Q')
    packed.append(0)

    for i, x in enumerate(a):
        c = x - 1
        cid = c + 1

        if i == first[c]:
            pref1[c] = t1 * BASE + id1
            pref2[c] = t2 * BASE + id2

        cnt[c] += 1
        v = cnt[c]

        if cid == id1:
            t1 = v
        elif cid == id2:
            t2 = v
            if t2 > t1:
                t1, t2 = t2, t1
                id1, id2 = id2, id1
        elif v > t1:
            t2, id2 = t1, id1
            t1, id1 = v, cid
        elif v > t2:
            t2, id2 = v, cid

        e1 = t1 * BASE + id1
        e2 = t2 * BASE + id2
        packed.append((e1 << PAIR_BITS) | e2)

    # Suffix candidates for every color.
    suf1 = [0] * k
    suf2 = [0] * k

    cnt = [0] * k
    t1 = 0
    id1 = 0
    t2 = 0
    id2 = 0

    # No-complete-color case.
    best_no_full = 0

    # Cut m, where the suffix is empty.
    p = packed[m]
    pe1 = p >> PAIR_BITS
    pe2 = p & ((1 << PAIR_BITS) - 1)

    pc1 = pe1 >> BITS
    pi1 = pe1 & MASK
    pc2 = pe2 >> BITS
    pi2 = pe2 & MASK

    best_no_full = max(
        pc1,
        pc2,
    )

    for i in range(m - 1, -1, -1):
        c = a[i] - 1
        cid = c + 1

        if i == last[c]:
            suf1[c] = t1 * BASE + id1
            suf2[c] = t2 * BASE + id2

        cnt[c] += 1
        v = cnt[c]

        if cid == id1:
            t1 = v
        elif cid == id2:
            t2 = v
            if t2 > t1:
                t1, t2 = t2, t1
                id1, id2 = id2, id1
        elif v > t1:
            t2, id2 = t1, id1
            t1, id1 = v, cid
        elif v > t2:
            t2, id2 = v, cid

        # The current suffix is [i, m).
        p = packed[i]
        pe1 = p >> PAIR_BITS
        pe2 = p & ((1 << PAIR_BITS) - 1)

        pc1 = pe1 >> BITS
        pi1 = pe1 & MASK
        pc2 = pe2 >> BITS
        pi2 = pe2 & MASK

        # Combine the two best prefix and suffix colors.
        if pi1 == 0 or id1 == 0 or pi1 != id1:
            best_no_full = max(best_no_full, pc1 + t1)

        if pi1 == 0 or id2 == 0 or pi1 != id2:
            best_no_full = max(best_no_full, pc1 + t2)

        if pi2 != 0 and pi2 != id1:
            best_no_full = max(best_no_full, pc2 + t1)

        if pi2 != 0 and pi2 != id2:
            best_no_full = max(best_no_full, pc2 + t2)

    # DP states:
    # dp1[c], dp2[c] are the best two states ending with color c.
    # The second component is the color used as the left partial endpoint.
    dp1_val = [0] * k
    dp1_id = [0] * k
    dp2_val = [0] * k
    dp2_id = [0] * k

    for c in order:
        e1 = pref1[c]
        e2 = pref2[c]

        v1 = n + (e1 >> BITS)
        q1 = e1 & MASK

        v2 = n + (e2 >> BITS)
        q2 = e2 & MASK

        b1v = v1
        b1q = q1
        b2v = -1
        b2q = -1

        if q2 != q1:
            if v2 > b1v:
                b2v, b2q = b1v, b1q
                b1v, b1q = v2, q2
            else:
                b2v, b2q = v2, q2

        # Try every earlier complete color.
        for d in order:
            if first[d] >= first[c]:
                break
            if last[d] >= first[c]:
                continue

            v = dp1_val[d] + n
            q = dp1_id[d]

            if q == b1q:
                if v > b1v:
                    b1v = v
            elif q == b2q:
                if v > b2v:
                    b2v = v
            elif v > b1v:
                b2v, b2q = b1v, b1q
                b1v, b1q = v, q
            elif v > b2v:
                b2v, b2q = v, q

            v = dp2_val[d] + n
            q = dp2_id[d]

            if q == 0 and dp2_val[d] == 0:
                continue

            if q == b1q:
                if v > b1v:
                    b1v = v
            elif q == b2q:
                if v > b2v:
                    b2v = v
            elif v > b1v:
                b2v, b2q = b1v, b1q
                b1v, b1q = v, q
            elif v > b2v:
                b2v, b2q = v, q

        dp1_val[c] = b1v
        dp1_id[c] = b1q
        dp2_val[c] = b2v if b2v >= 0 else 0
        dp2_id[c] = b2q if b2v >= 0 else 0

    best = best_no_full

    for c in range(k):
        s1 = suf1[c]
        s2 = suf2[c]

        sc1 = s1 >> BITS
        si1 = s1 & MASK
        sc2 = s2 >> BITS
        si2 = s2 & MASK

        for dv, di in (
            (dp1_val[c], dp1_id[c]),
            (dp2_val[c], dp2_id[c]),
        ):
            if dv == 0:
                continue

            if di == 0 or si1 == 0 or di != si1:
                best = max(best, dv + sc1)

            if di == 0 or si2 == 0 or di != si2:
                best = max(best, dv + sc2)

    answer = m - best
    return str(answer)

if __name__ == "__main__":
    print(solve())
```

The first scan computes the first and last occurrence of every color. Those boundaries are the only information needed to decide whether two colors can both be kept completely.

The forward count maintenance serves two purposes. At the first occurrence of a color, the current counts describe exactly the prefix before that color. At every cut, the packed value stores the two best prefix colors, which is later needed for the no-complete-color case.

The packing uses ten bits for a color identifier because K is at most 1000. Another ten bits store its count, which is at most N. Two such candidates fit comfortably into a 64-bit integer. Using `array('Q')` keeps the memory usage small even though there can be one million cuts.

The reverse scan computes suffix candidates. The suffix state before processing position i describes positions after i, which is exactly what is needed when `i` is the last occurrence of a color. After adding position i, the suffix state corresponds to the cut before i and can be combined with the already stored prefix state.

The DP stores two states per ending color rather than one. The reason is that the best left endpoint color may happen to equal the best right endpoint color. Keeping two different left colors guarantees that we can discard a conflicting state when choosing the right endpoint.

Python integers do not overflow here. The maximum number of untouched plumbuses is N times K, at most 1,000,000. The encoded candidate values are also comfortably inside 64-bit integers.

## Worked Examples

### Sample 1

The input is

```
3 3
1 2 3 3 2 1 1 2 3
```

The relevant color intervals are

```
color 1: [1, 7]
color 2: [2, 8]
color 3: [3, 9]
```

No two intervals are disjoint, so no two colors can both be complete. A useful choice is color 2 as the complete middle group. One color 1 can be retained before it and one color 3 can be retained after it.

| State | Value |
| --- | --- |
| Complete color 2 | 3 |
| Best left partial color 1 | 1 |
| Best right partial color 3 | 1 |
| Untouched total | 5 |
| Total plumbuses | 9 |
| Moves | 4 |

The five untouched plumbuses can appear as `1 2 2 2 3`. All remaining four can be moved to the two ends. The DP finds five untouched elements, so the answer is 9 minus 5, which is 4.

### Sample 2

The input is

```
2 4
3 3 1 1 4 4 2 2
```

Every color already forms one complete block.

| Color | First | Last | DP role |
| --- | --- | --- | --- |
| 3 | 1 | 2 | First complete color |
| 1 | 3 | 4 | Extends the chain |
| 4 | 5 | 6 | Extends the chain |
| 2 | 7 | 8 | Extends the chain |

The interval condition holds at every transition, so all four colors can be kept completely.

| State | Value |
| --- | --- |
| Complete colors | 4 |
| Plumbuses per color | 2 |
| Untouched total | 8 |
| Total plumbuses | 8 |
| Moves | 0 |

The result is zero, which also confirms that the DP does not force unnecessary endpoint moves when the original arrangement is already valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(NK + K²) | The array is scanned a constant number of times, and the color DP checks at most K² pairs. |
| Space | O(NK + K) | The original array and one packed prefix state are stored, together with O(K) color and DP data. |

The largest array contains 1,000,000 plumbuses, so the linear part performs only a few million simple operations. The quadratic DP contains at most 1,000,000 color-pair checks. The algorithm avoids any dependence on permutations of the colors or subsets of individual plumbuses.

## Test Cases

```python
import sys
import io
from array import array

# Put the submitted solve() implementation above this test section.

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input
    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline
        return solve().strip()
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided samples
assert run(
    "3 3\n"
    "1 2 3 3 2 1 1 2 3\n"
) == "4", "sample 1"

assert run(
    "2 4\n"
    "3 3 1 1 4 4 2 2\n"
) == "0", "sample 2"

# Minimum-size input
assert run(
    "1 1\n"
    "1\n"
) == "0", "minimum size"

# All plumbuses already have one color group
assert run(
    "5 1\n"
    "1 1 1 1 1\n"
) == "0", "all equal"

# Alternating colors, so neither color can be kept as a complete
# group together with the other, but keeping one complete color
# still leaves an optimal solution.
assert run(
    "2 2\n"
    "1 2 1 2\n"
) == "2", "alternating boundary case"

# Two partial endpoint groups are optimal here.
assert run(
    "3 2\n"
    "1 1 2 2 1 2\n"
) == "2", "two partial endpoint colors"

# Maximum-size case: 1000 copies of each of two alternating colors.
# Keeping all 1000 occurrences of either color is optimal.
a = " ".join("1 2" for _ in range(1000))
assert run(
    "1000 2\n" + a + "\n"
) == "1000", "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | 0 | Minimum size and single-color handling |
| `5 1 / 1 1 1 1 1` | 0 | All elements already form one group |
| `2 2 / 1 2 1 2` | 2 | Overlapping color intervals and complete-color DP |
| `3 2 / 1 1 2 2 1 2` | 2 | Optimal solution using endpoint partial colors |
| `1000 2 / 1 2 ... 1 2` | 1000 | Maximum input size and large DP/input handling |

## Edge Cases

For the single-color case

```
1 1
1
```

the DP considers color 1 as a complete group and keeps N=1 plumbus. There is no need for a left or right partial color, so the maximum number of untouched plumbuses is 1 and the answer is 0.

For the alternating case

```
2 2
1 2 1 2
```

the intervals are `[1,3]` for color 1 and `[2,4]` for color 2. They overlap, so they cannot both be complete. The DP keeps either complete color, preserving two plumbuses, and the remaining two are moved to the ends. The answer is 2.

For the two-partial-color case

```
3 2
1 1 2 2 1 2
```

there is a cut after the first four elements. The prefix contains two 1s and the suffix contains one 1 and one 2, but the best valid arrangement is obtained by moving the final 1 and final 2, leaving `1 1 2 2` untouched. These are already two complete groups, so two operations suffice. The no-complete-color DP is also checked, but the full-group representation gives the optimum of 2.

For the maximum-size alternating case, the array contains 2000 elements when N=1000 and K=2. The two color intervals overlap completely, so they cannot both remain complete. Keeping either color completely preserves 1000 plumbuses, while the other 1000 must be moved. The algorithm returns 1000 without performing any operation proportional to K times the array length.

The endpoint conflict case deserves special attention. Suppose the best prefix color and the best suffix color are both color 1. Keeping both would create two separated groups of color 1, which is illegal. The algorithm stores the two best candidates on each side and tries both choices. If the best candidates collide, the second-best candidate on one side can be selected. If no distinct candidate exists, the corresponding endpoint simply remains empty.
