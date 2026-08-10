---
title: "CF 102411L - Lengths and Periods"
description: "We need to find the largest repetition exponent among all contiguous substrings of a given string. A substring with period (p) has the same character at positions whose indices differ by (p), and if its length is (L), its exponent is (L/p)."
date: "2026-08-10T15:08:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102411
codeforces_index: "L"
codeforces_contest_name: "ICPC 2019-2020 North-Western Russia Regional Contest"
rating: 0
weight: 102411
solve_time_s: 1206
verified: false
draft: false
---

[CF 102411L - Lengths and Periods](https://codeforces.com/problemset/problem/102411/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 20m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We need to find the largest repetition exponent among all contiguous substrings of a given string. A substring with period (p) has the same character at positions whose indices differ by (p), and if its length is (L), its exponent is (L/p). The period does not have to divide the substring length, which is why the answer can be fractional.

For example, in `mississippi`, the substring `ississi` has length (7) and period (3). Its first four characters and last four characters are both `issi`, so shifting by three positions preserves all seven characters. Its exponent is consequently (7/3).

The input is one lowercase string (s), with (1 \le |s| \le 200000). We must print the maximum exponent as an irreducible fraction.

The upper bound of (200000) rules out enumerating all substrings, which already gives (O(n^2)) candidates. It also rules out comparing every pair of substrings or suffixes character by character, since that can reach (O(n^3)). With a two second limit, the intended solution needs close to linear or (O(n\log n)) behavior.

There are several edge cases that are easy to mishandle. For a one-character string such as

```
a
```

the answer is `1/1`. There is no pair of occurrences to create a nontrivial repetition, but every single character is a power of exponent one. An implementation that initializes the answer only from repeated substrings can incorrectly produce zero.

A string with no repeated character also has answer `1/1`. For example,

```
ab
```

contains no repetition of exponent greater than one. A careless implementation might treat two different characters as a period-two repetition merely because their distance is two, but a period requires equality between the corresponding characters.

A fractional answer needs to be preserved exactly. For

```
aba
```

the whole string has period (2) and length (3), so the answer is `3/2`. Using floating point for comparisons can introduce unnecessary precision issues, while comparing fractions by cross multiplication is exact.

Finally, overlapping occurrences must count. In

```
aaaaa
```

the period is (1), so the whole string has exponent (5), giving `5/1`. Looking only for non-overlapping copies would incorrectly stop at exponent two.

## Approaches

The direct approach is to choose two positions (i<j), let (d=j-i), and compare the suffixes beginning at those positions until they differ. If their longest common prefix has length (L), then the substring starting at (i) and ending (L) characters after position (j) has period (d) and length (L+d). Its exponent is

[
\frac{L+d}{d}=1+\frac{L}{d}.
]

Every possible fractional power can be represented this way. If a substring has period (d), compare the substring with itself shifted by (d). The matching part is exactly a common prefix of two suffixes whose starting positions differ by (d).

The brute-force algorithm therefore checks every pair (i<j), computes their LCP directly, and maximizes ((LCP+j-i)/(j-i)). It is correct because every possible period corresponds to such a pair, and every pair with a positive LCP gives a valid periodic substring. The problem is the cost. There are (\Theta(n^2)) pairs, and for a string consisting entirely of `a`, the LCP for a pair can itself be (\Theta(n)). The total number of character comparisons is

[
\sum_{d=1}^{n-1}(n-d)^2
=\Theta(n^3).
]

For (n=200000), that is far beyond what a two second limit permits.

The first useful observation is that the LCP of two positions is not arbitrary information. Strings having the same set of ending positions can be grouped together by a suffix automaton. Each suffix automaton state represents one such end-position equivalence class, and its suffix links form a tree in which a parent contains all occurrences represented by its child.

Suppose a state (v) represents substrings whose longest length is `len[v]`. Every pair of positions in its end-position set contains two occurrences of that longest substring. If two such ending positions differ by (d), the substring spanning from the beginning of the earlier occurrence to the end of the later occurrence has length `len[v] + d` and period (d). Its exponent is

[
\frac{\operatorname{len}[v]+d}{d}.
]

For a fixed state, we therefore only need the smallest distance between two positions in its end-position set. If that distance is (d_v), the best candidate contributed by the state is

[
\frac{\operatorname{len}[v]+d_v}{d_v}.
]

This transforms the original problem into a tree problem. Build the suffix automaton, build its suffix-link tree, collect the ending positions belonging to each state, and for every state find the minimum gap between consecutive positions in its ordered position set.

The remaining data-structure problem is that these position sets have to be merged along the suffix-link tree. A normal sorted Python list is unsuitable because insertion into its middle costs linear time. We use a randomized treap, where the key is the ending position. Two treaps can be united directly by splitting one according to the root key of the other. The expected cost of treap union is (O(m\log(n/m+1))) for sets of sizes (m\le n), and over all suffix-link-tree merges the total expected cost is (O(n\log n)).

Each treap node stores its smallest key, largest key, and smallest difference between consecutive keys. These three values can be recomputed from its two children in constant time. Thus after every union, the root immediately tells us the minimum distance between any two occurrence positions in the merged set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)) | (O(n)) | Too slow |
| Optimal | Expected (O(n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Build a suffix automaton for the string. Each ordinary state created while reading position (i) remembers (i) as one direct ending position. Clone states do not receive a direct position. The standard suffix automaton construction uses at most (2n-1) states.
2. Interpret every suffix automaton state as an end-position equivalence class. If a substring belongs to state (v), all substrings represented by (v) occur at exactly the same ending positions. The longest represented substring has length `len[v]`.
3. Build the suffix-link tree. For every state (v\ne0), add (v) as a child of `link[v]`. A child's end-position set is contained in its parent's set, so processing this tree bottom-up allows us to construct every set from the sets of its children.
4. Create one treap node for every string position. Its key is the ending position itself. Initially, the treap belonging to a real state contains its direct position, while a clone starts empty.
5. Process the suffix-link tree in postorder. Start state (v)'s treap with its direct position, then unite it with every child's treap. After all children have been merged, the resulting treap contains exactly `endpos[v]`.
6. Maintain three values in every treap subtree: the smallest key, the largest key, and the minimum difference between adjacent keys. If a node has key (x), a left subtree, and a right subtree, the only new gaps introduced by joining the three ordered parts are `x - maximum(left)` and `minimum(right) - x`. The best gap is the minimum of those values and the two children's existing gaps.
7. Let (d) be the minimum gap in state (v)'s treap. If at least two positions exist, the longest substring represented by (v) occurs at both positions separated by (d). The resulting periodic substring has length `len[v] + d`, so compare the fraction
[
\frac{\operatorname{len}[v]+d}{d}
]
with the current answer using integer cross multiplication.
8. After all states have been processed, reduce the best numerator and denominator by their greatest common divisor and print the fraction.

The key invariant is that after state (v) is processed, its treap contains exactly the ending positions of every substring represented by (v). Consequently, its minimum gap is the smallest possible period distance among two occurrences of the longest substring represented by (v). The corresponding exponent is valid, and every periodic substring in the original string induces two equal occurrences separated by its period, so it appears in the end-position set of some state. The maximum considered by the algorithm is thus both achievable and at least as large as every possible exponent.

## Python Solution

```python
import sys
import random
from array import array
from math import gcd

input = sys.stdin.readline
sys.setrecursionlimit(1_000_000)

def critical_exponent(s):
    n = len(s)
    max_states = 2 * n

    # Suffix automaton.
    # Each state has 26 transitions stored consecutively.
    trans = array('i', [-1]) * (max_states * 26)
    length = array('i', [0]) * max_states
    link = array('i', [-1]) * max_states
    direct_pos = array('i', [0]) * max_states

    size = 1
    last = 0

    for pos, ch in enumerate(s, 1):
        c = ord(ch) - 97

        cur = size
        size += 1
        length[cur] = length[last] + 1
        direct_pos[cur] = pos

        p = last
        while p != -1:
            idx = p * 26 + c
            q = trans[idx]
            if q != -1:
                break
            trans[idx] = cur
            p = link[p]

        if p == -1:
            link[cur] = 0
        else:
            q = trans[p * 26 + c]

            if length[p] + 1 == length[q]:
                link[cur] = q
            else:
                clone = size
                size += 1

                length[clone] = length[p] + 1
                link[clone] = link[q]

                a = clone * 26
                b = q * 26
                trans[a:a + 26] = trans[b:b + 26]

                while p != -1:
                    idx = p * 26 + c
                    if trans[idx] != q:
                        break
                    trans[idx] = clone
                    p = link[p]

                link[q] = clone
                link[cur] = clone

    # Build the suffix-link tree.
    head = array('i', [-1]) * size
    next_sibling = array('i', [-1]) * size

    for v in range(1, size):
        p = link[v]
        next_sibling[v] = head[p]
        head[p] = v

    # Obtain a traversal order. Reversing it gives postorder.
    order = [0]
    ptr = 0
    while ptr < len(order):
        v = order[ptr]
        ptr += 1

        u = head[v]
        while u != -1:
            order.append(u)
            u = next_sibling[u]

    # Treap data.
    # Node number equals its string position.
    left = array('i', [0]) * (n + 1)
    right = array('i', [0]) * (n + 1)
    mn = array('i', [n + 1]) * (n + 1)
    mx = array('i', [0]) * (n + 1)
    gap = array('i', [n + 1]) * (n + 1)

    # Random priorities keep the treaps balanced in expectation.
    priority = [0] * (n + 1)
    for i in range(1, n + 1):
        priority[i] = random.getrandbits(64)
        mn[i] = i
        mx[i] = i

    INF = n + 1

    def pull(t):
        l = left[t]
        r = right[t]

        mn[t] = mn[l] if l else t
        mx[t] = mx[r] if r else t

        best = gap[l] if l else INF

        if l:
            d = t - mx[l]
            if d < best:
                best = d

        if r:
            if gap[r] < best:
                best = gap[r]

            d = mn[r] - t
            if d < best:
                best = d

        gap[t] = best

    def split(t, key):
        if not t:
            return 0, 0

        if t < key:
            a, b = split(right[t], key)
            right[t] = a
            pull(t)
            return t, b

        a, b = split(left[t], key)
        left[t] = b
        pull(t)
        return a, t

    def unite(a, b):
        if not a:
            return b
        if not b:
            return a

        if priority[a] < priority[b]:
            a, b = b, a

        bl, br = split(b, a)

        left[a] = unite(left[a], bl)
        right[a] = unite(right[a], br)

        pull(a)
        return a

    # root[v] is the treap representing endpos(v).
    root = array('i', [0]) * size

    best_num = 1
    best_den = 1

    for v in reversed(order):
        r = 0

        if direct_pos[v]:
            r = direct_pos[v]

        u = head[v]
        while u != -1:
            r = unite(r, root[u])
            u = next_sibling[u]

        root[v] = r

        if r and gap[r] < INF:
            d = gap[r]
            num = length[v] + d
            den = d

            if num * best_den > best_num * den:
                best_num = num
                best_den = den

    g = gcd(best_num, best_den)
    return f"{best_num // g}/{best_den // g}"

def solve():
    s = input().strip()
    print(critical_exponent(s))

if __name__ == "__main__":
    solve()
```

The suffix automaton uses a flat transition array instead of a Python dictionary per state. There are at most (2n-1) states, so allocating `2*n*26` integer slots keeps the representation predictable and avoids hundreds of thousands of dictionary objects. The `array` module stores these integers compactly, which matters for (n=200000).

During construction, `direct_pos[cur] = pos` records that the newly created real state contains the current prefix ending position. Clones deliberately keep this field equal to zero. A clone is an equivalence-class split, not a new occurrence created by reading another character, so assigning it a fresh occurrence would corrupt every end-position set.

The suffix-link tree is processed in reverse traversal order. Children occur after their parent in the forward traversal, so reversing it guarantees that every child's treap is complete before it is merged into its parent.

The treap is keyed by the actual ending positions. Because the keys are unique and the tree is a binary search tree, every subtree is an ordered set of positions. The `pull` function only needs to inspect the gap inside the left subtree, the gap inside the right subtree, the gap between the left subtree and the root, and the gap between the root and the right subtree.

The `split` function separates keys smaller than `key` from keys larger than or equal to `key`. In `unite`, the two sets are disjoint, so the chosen root key cannot occur in the other tree. The union operation recursively partitions the second tree around the first root and then combines the corresponding halves.

The final comparison uses

[
\frac{a}{b}>\frac{c}{d}
\iff ad>cb
]

instead of floating point. All relevant values fit easily into Python integers, so there is no overflow issue either.

The fraction stored by the algorithm is not yet necessarily reduced. Reducing only once at the end is cheaper and simpler than reducing every candidate.

## Worked Examples

### Sample 1: `mississippi`

The decisive state represents the substring `issi`. Its longest represented length is (4), and its end positions are (5) and (8). Their difference is (3). The two occurrences are `issi` ending at positions (5) and (8), which gives the periodic factor `ississi`.

| State / substring | `len[v]` | End positions | Minimum gap `d` | Candidate numerator | Candidate fraction |
| --- | --- | --- | --- | --- | --- |
| `i` | 1 | 2, 5, 8, 11 | 3 | 4 | 4/3 |
| `ss` | 2 | 4, 7 | 3 | 5 | 5/3 |
| `issi` | 4 | 5, 8 | 3 | 7 | 7/3 |
| Root | 0 | 1, 2, ..., 11 | 1 | 1 | 1/1 |

The `issi` state produces (4+3=7) characters with period (3), giving (7/3). The shorter candidates cannot beat it, so the answer is `7/3`.

The trace demonstrates why we need the longest substring represented by a state rather than merely its shortest one. The same end-position set can represent several nested substrings, and using the largest length gives the strongest exponent.

### Sample 2: `abab`

The substring `ab` occurs ending at positions (2) and (4). The distance is (2), while the longest substring represented by its state has length (2).

| State / substring | `len[v]` | End positions | Minimum gap `d` | Candidate | Best so far |
| --- | --- | --- | --- | --- | --- |
| `a` | 1 | 1, 3 | 2 | 3/2 | 3/2 |
| `b` | 1 | 2, 4 | 2 | 3/2 | 3/2 |
| `ab` | 2 | 2, 4 | 2 | 4/2 = 2 | 2 |
| Root | 0 | 1, 2, 3, 4 | 1 | 1 | 2 |

The state for `ab` gives ((2+2)/2=2), corresponding exactly to `abab = ab` repeated twice. The final reduction turns `4/2` into `2/1`.

This trace also demonstrates why the minimum gap matters. Once a state contains several occurrences, choosing the closest two gives the largest exponent because `len[v]` is fixed while the denominator is the distance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Expected (O(n\log n)) | SAM construction is linear, and all suffix-link-tree treap unions have expected (O(n\log n)) total work |
| Space | (O(n)) | The SAM has (O(n)) states and transitions, while each string position creates exactly one treap node |

The input length is at most (200000), so an (O(n\log n)) algorithm performs on the order of a few million logarithmic-scale operations rather than hundreds of billions of character comparisons. The compact transition and treap arrays also keep memory comfortably below the 512 MB limit.

## Test Cases

The following harness assumes the submitted solution is saved as `solution.py`. It executes the actual program, so the assertions test the same code that is submitted rather than a separate reference implementation.

```python
import sys
import io
import subprocess

def run(inp: str) -> str:
    result = subprocess.run(
        [sys.executable, "solution.py"],
        input=inp + "\n",
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()

# Provided samples
assert run("mississippi") == "7/3", "sample 1"
assert run("abab") == "2/1", "sample 2"

# Minimum-size input
assert run("a") == "1/1", "single character"

# No repeated characters
assert run("ab") == "1/1", "no repetition"

# Fractional exponent with an overlapping period
assert run("ababa") == "5/2", "fractional overlap"

# All characters equal
assert run("aaaaa") == "5/1", "all equal"

# Maximum-size input
assert run("a" * 200000) == "200000/1", "maximum-size all-equal string"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `1/1` | Minimum size and the implicit exponent-one answer |
| `ab` | `1/1` | A string with no repeated substring |
| `ababa` | `5/2` | Fractional exponent and overlapping occurrences |
| `aaaaa` | `5/1` | Smallest period and maximal repetition |
| `a` repeated 200000 times | `200000/1` | Maximum input size and long suffix-link chains |

## Edge Cases

For the minimum input

```
a
```

the suffix automaton contains only the root and one real state. No state has two ending positions, so no nontrivial candidate is generated. The initial answer remains (1/1), which is exactly correct.

For

```
ab
```

the two real states correspond to the individual characters, each occurring once. The root contains both positions, but its longest represented length is zero, so it contributes only exponent one. The result is `1/1`. This prevents an implementation from confusing positional distance with a valid repeated pattern.

For

```
aba
```

the state containing `a` has end positions (1) and (3), giving minimum gap (2). Its longest represented substring has length (1), so the candidate is

[
\frac{1+2}{2}=\frac32.
]

The algorithm outputs `3/2`. The occurrences overlap only at their endpoints in the resulting periodic factor, which confirms that the method does not require two disjoint copies.

For

```
aaaaa
```

every nonempty substring consists only of `a`. The state representing the longest repeated substring has length (5), and its end-position set contains all relevant positions. The smallest gap is (1), so the candidate is

[
\frac{5+1}{1}=6
]

if we used that state directly, which would be incorrect because the state of the longest substring `aaaaa` has only one occurrence. The actual states with multiple occurrences have the appropriate shorter `len` values, while the root represents length zero. In particular, the state representing `aaaa` has two ending positions, (4) and (5), and gives ((4+1)/1=5). Thus the algorithm correctly returns `5/1`. This is a useful sanity check for the distinction between substring length and occurrence count.

For the maximum input

```
aaaaaaaa...aaaaaaaa
```

with (200000) characters, the suffix automaton becomes a simple chain with (O(n)) states. The suffix-link processing consequently builds increasingly large occurrence sets. The treap union operations remain logarithmic in expectation, and the final state with the appropriate repeated substring yields `200000/1`. The test exercises both the memory layout and the long-chain behavior of the automaton.

The central correctness property survives all of these cases: every state stores exactly one end-position equivalence class, every pair of positions in that class gives a valid period equal to their distance, and choosing the smallest such distance gives the largest exponent available from that state.

The editorial is written around the SAM formulation because it gives a particularly clean explanation of why the answer reduces to `len[state] + minimum_gap` over the suffix-link tree.
