---
title: "CF 102411L - Lengths and Periods"
description: "We have a string w of length at most 200000. We want to find the most repetitive substring inside it, where the repetition is allowed to stop halfway through the next copy. Suppose a substring has period p and length L. Its exponent is L / p."
date: "2026-08-11T07:53:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102411
codeforces_index: "L"
codeforces_contest_name: "ICPC 2019-2020 North-Western Russia Regional Contest"
rating: 0
weight: 102411
solve_time_s: 722
verified: true
draft: false
---

[CF 102411L - Lengths and Periods](https://codeforces.com/problemset/problem/102411/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 12m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string `w` of length at most `200000`. We want to find the most repetitive substring inside it, where the repetition is allowed to stop halfway through the next copy.

Suppose a substring has period `p` and length `L`. Its exponent is `L / p`. For example, `abababa` has period `2`, because every character agrees with the character two positions later wherever both positions exist. Its exponent is `7 / 2`. The task is to maximize this ratio over every substring and every valid period.

The answer is not necessarily an integer. A substring can contain several complete copies of a period and then a prefix of one more copy. The required output is the maximum ratio, reduced to lowest terms.

The length bound of `200000` rules out anything that explicitly examines all substrings and then compares their characters. There are already about `n²/2` substrings, so even constant work per substring is too much. An algorithm around `O(n log n)` is appropriate for the two second limit. The final solution uses an `O(n log n)` suffix array construction, linear-time LCP construction, and expected `O(n log n)` total work for the set unions.

There are several small cases that are easy to mishandle. For `a`, there is no pair of distinct suffixes and no repetition, but the answer is still `1/1`, because a single character has exponent one. A solution that initializes the answer to zero can accidentally produce an invalid fraction.

For `abc`, no substring has period shorter than its own length, so the answer is `1/1`. A solution that only searches for repeated pairs may find nothing and must still return one.

For `aba`, the whole string has period `2`: the first two characters are `ab`, and the remaining character is the prefix `a` of that period. Its exponent is `3/2`. A solution that only considers complete repetitions would miss this fractional answer and incorrectly return `1/1`.

For `aaaa`, the entire string has period `1`, giving exponent `4/1`. This case also exposes inefficient implementations because every pair of suffixes has a long common prefix. A character-by-character comparison over all pairs becomes cubic.

## Approaches

A direct approach can enumerate two positions `i < j` and regard `j - i` as a candidate period. We then compare `w[i:]` and `w[j:]` character by character to find their longest common prefix. If that LCP has length `L`, the substring beginning at `i` and ending after those `L` matching characters has length `L + (j-i)` and period `j-i`, so it gives exponent

[
\frac{L+(j-i)}{j-i}.
]

This is correct, because every valid repetition with period `p` gives two suffixes starting `p` positions apart whose common prefix contains everything except the first copy of the period.

The problem is the cost. There are `Theta(n²)` pairs `(i,j)`, and a single LCP comparison can take `Theta(n)` time. On a string such as `aaaa...a`, almost every comparison scans a linear number of characters. The total work is `Theta(n³)`, around `8 * 10^15` character comparisons when `n = 200000`, which is far beyond the limit.

The key observation is that we do not actually need to calculate every LCP independently. A suffix array puts all suffixes in lexicographic order, and the LCP of any two suffixes is the minimum LCP value on the interval between their ranks. If `height[k]` is the LCP of suffix-array entries `k-1` and `k`, then

[
LCP(i,j)=\min(height[r_i+1],\ldots,height[r_j]).
]

This turns the problem into a threshold connectivity problem.

Imagine processing the `height` values from largest to smallest. When we reach a value `h`, connect every adjacent pair of suffixes whose LCP is at least `h`. A connected component now contains exactly the suffixes sharing a prefix of length at least `h`.

Inside such a component, we want two suffixes whose starting positions in the original string are as close as possible. If their positions differ by `d`, their LCP is at least `h`, so they produce a valid substring of length `h+d` with period `d`. Its exponent is

[
\frac{h+d}{d}.
]

For a fixed `h`, maximizing this ratio is exactly the same as minimizing `d`.

The remaining data-structure problem is maintaining the minimum distance between two original string positions in every DSU component. Since positions are integers, an ordered set is enough. When two components are merged, we need the minimum distance inside their union. We maintain each component as a randomized treap keyed by the original string position. Every treap node stores the first position, last position, and minimum gap between consecutive positions in its subtree. A treap union combines two disjoint ordered sets efficiently.

The suffix array supplies the LCP information, the descending scan supplies the correct threshold components, DSU maintains those components, and the treap maintains the closest pair of original positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n³)` | `O(n)` | Too slow |
| Optimal | Expected `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Build the suffix array of `w`. The suffix array contains every suffix starting position in lexicographic order. We use prefix doubling with counting sort, so every doubling round costs `O(n)` and there are `O(log n)` rounds.
2. Build the LCP array with Kasai's algorithm. For every suffix-array rank `r > 0`, `height[r]` stores the LCP of suffixes `sa[r-1]` and `sa[r]`. Kasai's reuse of the previous LCP makes the entire construction linear.
3. Interpret every `height[r]` as an edge between suffix-array positions `r-1` and `r`. An edge of value `h` says that those two suffixes share a prefix of length `h`.
4. Sort the positive LCP edges by decreasing height. Initially every suffix is its own DSU component. When processing an edge with value `h`, merge its two components. All suffixes in the resulting component share a prefix of length at least `h`.
5. Associate an ordered treap with every DSU component. The keys are the starting positions of the corresponding suffixes in the original string. Each treap stores the smallest difference between two keys in the component.
6. After merging an edge of height `h`, let `d` be the minimum distance stored by the resulting treap. Choose two suffixes whose starting positions differ by `d`. Their common prefix has length at least `h`, so the substring consisting of the first `d` characters followed by that common prefix has length `d+h` and period `d`. Its exponent is `(d+h)/d`.
7. Compare that fraction with the current best answer using cross multiplication. We compare `a/b` and `c/d` as `a*d` versus `c*b`, avoiding floating-point arithmetic entirely.
8. Ignore zero LCP values. They can only produce exponent `1`, which is already the initial answer `1/1`.
9. Reduce the final numerator and denominator by their greatest common divisor before printing. The denominator is always positive, and all intermediate values fit comfortably in Python integers.

### Why it works

Consider any two suffixes starting at positions `i < j`, and let `d = j-i`. If their LCP is `L`, then the characters at positions `i+k` and `j+k` are equal for every `0 <= k < L`. Since the second suffix starts exactly `d` characters later, the substring of length `d+L` starting at `i` has period `d`. Thus every suffix pair gives a valid exponent `(d+L)/d`.

Now consider any valid substring with period `p` and length `T`. Its first `T-p` characters are equal to the substring beginning `p` positions later, so the suffixes at its first two period positions have LCP at least `T-p`. Taking those two positions gives a candidate exponent at least

[
\frac{p+(T-p)}p=\frac Tp.
]

Thus an optimal answer is represented by some pair of suffixes.

For a fixed LCP threshold `h`, suffixes are in the same DSU component exactly when every LCP edge between their suffix-array ranks is at least `h`. Consequently, any pair in that component has LCP at least `h`. The smallest original-position distance `d` in the component gives the largest possible `(h+d)/d` among pairs known to have LCP at least `h`.

When the actual LCP of an optimal pair is `L`, the scan eventually reaches height `L`. At that moment the pair belongs to one component, so its distance is considered. Hence the algorithm cannot miss the optimum. Every candidate it produces corresponds to an actual periodic substring, so it cannot produce an invalid answer either.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1_000_000)

INF = 10**18

def suffix_array(s):
    n = len(s)

    # Append a unique sentinel smaller than every real character.
    a = [c - 96 for c in s] + [0]
    m = n + 1

    # Initial sorting by character using counting sort.
    alphabet = 27
    cnt = [0] * alphabet
    for x in a:
        cnt[x] += 1

    for i in range(1, alphabet):
        cnt[i] += cnt[i - 1]

    p = [0] * m
    for i in range(m - 1, -1, -1):
        x = a[i]
        cnt[x] -= 1
        p[cnt[x]] = i

    c = [0] * m
    classes = 1
    c[p[0]] = 0

    for i in range(1, m):
        if a[p[i]] != a[p[i - 1]]:
            classes += 1
        c[p[i]] = classes - 1

    k = 1

    while k < m and classes < m:
        # Shift every cyclic suffix by k.
        shifted = [0] * m
        for i in range(m):
            x = p[i] - k
            if x < 0:
                x += m
            shifted[i] = x

        # Counting-sort shifted positions by their class.
        cnt = [0] * classes
        for x in shifted:
            cnt[c[x]] += 1

        total = 0
        for i in range(classes):
            v = cnt[i]
            cnt[i] = total
            total += v

        new_p = [0] * m
        for x in shifted:
            cls = c[x]
            new_p[cnt[cls]] = x
            cnt[cls] += 1

        p = new_p

        new_c = [0] * m
        new_classes = 1
        new_c[p[0]] = 0

        for i in range(1, m):
            cur = p[i]
            prev = p[i - 1]

            cur_pair = (c[cur], c[(cur + k) % m])
            prev_pair = (c[prev], c[(prev + k) % m])

            if cur_pair != prev_pair:
                new_classes += 1

            new_c[cur] = new_classes - 1

        c = new_c
        classes = new_classes
        k <<= 1

    # The sentinel itself is first and is not a suffix of the original string.
    return p[1:]

def build_lcp(s, sa):
    n = len(s)
    rank = [0] * n

    for i, pos in enumerate(sa):
        rank[pos] = i

    height = [0] * n
    h = 0

    for i in range(n):
        r = rank[i]

        if r == 0:
            continue

        j = sa[r - 1]

        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1

        height[r] = h

        if h:
            h -= 1

    return height

def solve(s):
    n = len(s)

    if n == 1:
        return "1/1"

    sa = suffix_array(s)
    height = build_lcp(s, sa)

    # Treap arrays. Node i represents original string position i.
    left = [0] * n
    right = [0] * n
    priority = [0] * n

    first = list(range(n))
    last = list(range(n))
    min_gap = [INF] * n

    # Deterministic 32-bit pseudo-random priorities.
    seed = 0x12345678
    for i in range(n):
        seed = (seed * 1664525 + 1013904223) & 0xffffffff
        priority[i] = seed

    def pull(t):
        l = left[t]
        r = right[t]

        if l:
            first[t] = first[l]
        else:
            first[t] = t

        if r:
            last[t] = last[r]
        else:
            last[t] = t

        g = INF

        if l:
            if min_gap[l] < g:
                g = min_gap[l]
            d = t - last[l]
            if d < g:
                g = d

        if r:
            if min_gap[r] < g:
                g = min_gap[r]
            d = first[r] - t
            if d < g:
                g = d

        min_gap[t] = g

    def split(t, key):
        # All keys in the first result are < key.
        # All keys in the second result are > key.
        # key itself is guaranteed not to occur in t.
        if not t:
            return 0, 0

        if key < t:
            a, b = split(left[t], key)
            left[t] = b
            pull(t)
            return a, t
        else:
            a, b = split(right[t], key)
            right[t] = a
            pull(t)
            return t, b

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

    # DSU over suffix-array ranks.
    parent = list(range(n))
    treap_root = list(sa)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def merge_components(a, b):
        a = find(a)
        b = find(b)

        if a == b:
            return a

        parent[b] = a
        treap_root[a] = unite(treap_root[a], treap_root[b])
        treap_root[b] = 0

        return a

    # Each positive height is an edge between ranks idx-1 and idx.
    edges = [i for i in range(1, n) if height[i] > 0]
    edges.sort(key=height.__getitem__, reverse=True)

    best_num = 1
    best_den = 1

    for idx in edges:
        h = height[idx]

        root = merge_components(idx - 1, idx)
        d = min_gap[treap_root[root]]

        # The component contains at least two suffixes here,
        # so d is finite and positive.
        num = h + d
        den = d

        if num * best_den > best_num * den:
            best_num = num
            best_den = den

    g = __import__("math").gcd(best_num, best_den)
    return f"{best_num // g}/{best_den // g}"

def main():
    s = input().strip().encode()
    sys.stdout.write(solve(s) + "\n")

if __name__ == "__main__":
    main()
```

The suffix-array routine first appends a sentinel represented by zero. Sorting cyclic shifts of `w + sentinel` is equivalent to sorting the suffixes of `w`, because the sentinel is unique and smaller than every real character. Prefix doubling then replaces prefixes of length `k` by equivalence classes and sorts prefixes of length `2k` using two class values.

The LCP routine is Kasai's algorithm. `rank[i]` gives the suffix-array position of the suffix starting at `i`. When comparing it with the previous suffix in lexicographic order, the previous LCP value gives a lower bound for the new comparison, so the total number of character comparisons is linear.

The treap has one node per original string position. The node's key is simply its index, so no separate key array is needed. `first`, `last`, and `min_gap` summarize the ordered set represented by a subtree. The minimum gap can only be inside the left subtree, inside the right subtree, between the current key and the largest key on the left, or between the current key and the smallest key on the right.

`split` separates a treap by a key. The key used by `unite` is always absent from the other treap because the DSU components contain disjoint suffix positions. `unite` keeps the root with larger random priority and splits the other tree around that root's key. This is the standard randomized treap set-union operation.

The DSU is indexed by suffix-array rank, not by original string position. That distinction is essential. The edges being activated are between adjacent suffixes in lexicographic order, while the distance used in the exponent formula is between their original starting positions.

The answer comparison uses multiplication rather than division. For example, to compare `7/3` and `2/1`, the code checks `7*1 > 2*3`. Python integers do not overflow, but using exact integer arithmetic also avoids the precision problems that floating-point comparison would introduce.

The code deliberately initializes the answer to `1/1`. A string without any repeated character pattern has no positive LCP edge, but its critical exponent is still one.

## Worked Examples

### Sample 1: `mississippi`

Using zero-based positions, the suffix array is

`[10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]`.

The corresponding LCP array is

`[0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]`.

The algorithm processes positive heights in decreasing order.

| Edge index | Height `h` | Newly merged suffix positions | Minimum distance `d` | Candidate | Best so far |
| --- | --- | --- | --- | --- | --- |
| 3 | 4 | `{4, 1}` | 3 | `7/3` | `7/3` |
| 10 | 3 | `{5, 2}` | 3 | `6/3 = 2` | `7/3` |
| 8 | 2 | `{6, 3}` | 3 | `5/3` | `7/3` |
| 1 | 1 | `{10, 7}` | 3 | `4/3` | `7/3` |
| 2 | 1 | `{10, 7, 4, 1}` | 3 | `4/3` | `7/3` |
| 6 | 1 | `{9, 8}` | 1 | `2/1` | `7/3` |
| 9 | 1 | `{6, 3, 5}` | 1 | `2/1` | `7/3` |

At height `4`, the suffixes beginning at positions `4` and `1` share the prefix `issi`. Their distance is `3`, so the substring beginning at position `1` has length `4+3=7` and period `3`. It is `ississi`, giving exponent `7/3`.

The later merge containing positions `9` and `8` finds the repeated substring `pp`, giving exponent `2`. It is a valid candidate, but it does not beat `7/3`.

### Sample 2: `abab`

The suffixes are ordered as

`ab`, `abab`, `b`, `bab`,

so the suffix array is `[2, 0, 3, 1]`. The LCP array is `[0, 2, 0, 1]`.

| Edge index | Height `h` | Newly merged positions | Minimum distance `d` | Candidate | Best so far |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | `{2, 0}` | 2 | `4/2 = 2` | `2/1` |
| 3 | 1 | `{3, 1}` | 2 | `3/2` | `2/1` |

The first merge uses positions `2` and `0`. Their suffixes share `ab`, so the distance is `2` and the resulting substring has length `4`. This gives the exact square `abab`, whose exponent is `2`.

The second merge represents the fractional repetition `bab`, which has period `2` and exponent `3/2`. It is smaller than the full square.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Expected `O(n log n)` | Prefix-doubling suffix array costs `O(n log n)`, Kasai costs `O(n)`, sorting LCP edges costs `O(n log n)`, and treap set unions take expected `O(n log n)` in total |
| Space | `O(n)` | Suffix-array arrays, LCP data, DSU arrays, and one treap node per string position |

The input contains at most `200000` characters, so quadratic enumeration is already too large and cubic comparison is completely infeasible. The solution performs only logarithmically many full passes during suffix-array construction and keeps every auxiliary structure linear in the string length. The randomized treap avoids needing a non-standard ordered-set library in Python.

## Test Cases

```
# Assume the submitted solution is saved as solution.py
from solution import solve

def run(inp: str) -> str:
    return solve(inp.strip().encode())

# Provided samples
assert run("mississippi") == "7/3", "sample 1"
assert run("abab") == "2/1", "sample 2"

# Minimum-size input
assert run("a") == "1/1", "single character"

# No repetition at all
assert run("abc") == "1/1", "all characters different"

# Fractional exponent
assert run("aba") == "3/2", "fractional repetition"

# Small repeated block, catches period and boundary handling
assert run("aab") == "2/1", "repeated pair at the beginning"

# All equal values
assert run("aaaaa") == "5/1", "all equal characters"

# Maximum-size input
assert run("a" * 200000) == "200000/1", "maximum-size all-equal string"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `1/1` | Minimum input and the no-edge case |
| `abc` | `1/1` | String with no repeated pattern |
| `aba` | `3/2` | Fractional exponent and partial final period |
| `aab` | `2/1` | Repetition ending exactly at a boundary |
| `aaaaa` | `5/1` | Longest possible exponent and many equal LCP values |
| `a * 200000` | `200000/1` | Maximum input size and large integer answer |

## Edge Cases

For the single-character input `a`, the suffix array contains only one suffix and the LCP array contains only zero. No DSU merge is performed. The initial answer remains `1/1`, which is exactly the exponent of the only non-empty substring.

For `abc`, every positive LCP value is absent. There is no pair of suffixes with a common first character, so no substring can have a period smaller than its own length. Again the initial `1/1` is preserved. A solution that assumes at least one positive LCP edge would fail here.

For `aba`, the suffixes starting at positions `0` and `2` have LCP `1`. Their distance is `2`, so the algorithm eventually activates the corresponding LCP threshold and obtains

[
\frac{1+2}{2}=\frac32.
]

The corresponding substring is `aba`. This is exactly why the algorithm must use `h+d`, rather than only `2d` or only complete repeated blocks.

For `aab`, the suffixes beginning at positions `0` and `1` have LCP `1`. Their distance is `1`, giving

[
\frac{1+1}{1}=2.
]

The substring is `aa`. This catches implementations that accidentally require the repeated substring to extend beyond the current suffix or that mishandle the final LCP position.

For `aaaaa`, every pair of suffixes has a long common prefix. At the largest useful LCP threshold, the closest two starting positions have distance `1`. The final merge reaches a component containing all five positions, and the candidate is

[
\frac{4+1}{1}=5.
]

Thus the answer is `5/1`. This case also demonstrates why the ordered structure must maintain the minimum original-position gap efficiently, because the suffix-array components can become very large.

For the maximum input consisting of `200000` copies of `a`, the same reasoning gives period `1` and length `200000`, so the answer is `200000/1`. The numerator is handled directly as an integer, and there is no floating-point calculation or fixed-width overflow concern.
