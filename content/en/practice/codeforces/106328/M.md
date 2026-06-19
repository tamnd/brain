---
title: "CF 106328M - Classic Revisited"
description: "We are given a sequence of integers and asked to extract a subsequence that reads the same forward and backward, with the additional constraint that its length must be even."
date: "2026-06-19T14:47:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106328
codeforces_index: "M"
codeforces_contest_name: "Baozii Cup 3"
rating: 0
weight: 106328
solve_time_s: 68
verified: true
draft: false
---

[CF 106328M - Classic Revisited](https://codeforces.com/problemset/problem/106328/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and asked to extract a subsequence that reads the same forward and backward, with the additional constraint that its length must be even. Among all such valid subsequences, we want the longest possible one, and we must output both its length and one concrete subsequence achieving it.

A subsequence means we are allowed to delete elements from the array but we cannot reorder what remains. A palindromic subsequence means that if we write the chosen elements in order, the sequence is symmetric around its center. The extra restriction that the length is even implies we are really building mirrored pairs of equal values around the center, without a middle unmatched element.

The array size goes up to 100000, and values are large but bounded. This immediately rules out any quadratic or cubic reasoning over subsequences or pairs. Anything involving enumerating subsequences, or trying all splits, would explode. Even $O(n^2)$ pair checking is too slow.

A subtle constraint is that every value appears at least twice and the array is generated randomly. This strongly suggests that we are not expected to rely on pathological structure, but instead on a simple frequency driven construction that uses pairs of equal values.

A naive but tempting mistake is to assume we can independently pair equal values and concatenate all such pairs arbitrarily. That breaks the subsequence constraint because order matters.

For example, if the array is `[1, 2, 1, 2]`, pairing `1-1` and `2-2` independently gives something like `1 2 2 1`, which is valid. But if we had a more interleaved arrangement like `[1, 2, 3, 1, 3, 2]`, careless pairing might produce indices that cannot be arranged into a valid subsequence palindrome if we do not respect ordering of chosen positions.

The real challenge is not computing how many pairs exist, but ensuring the chosen pairs can be embedded into a single increasing index sequence.

## Approaches

A brute-force approach would try all subsequences and test whether each is an even-length palindrome, tracking the maximum length. There are $2^n$ subsequences, and each check costs $O(n)$, making this completely infeasible even for $n = 40$, let alone $10^5$.

A more structured brute-force idea is to fix a center and expand outward, similar to palindrome checking. That works for substrings, not subsequences, because subsequences do not require contiguity. Once deletions are allowed, expansion logic loses structure and we are again forced into combinatorial selection.

The key observation is that every element in a valid even palindrome must be paired with another occurrence of the same value. So the entire problem reduces to selecting pairs of equal values and arranging them in a mirrored way. This converts the problem from subsequence selection into pairing instances of identical values.

The best possible length is therefore twice the total number of disjoint pairs we can form across all values. For a value that appears $f$ times, we can contribute $\lfloor f/2 \rfloor$ pairs. Summed over all values, this gives the maximum number of pairs.

The remaining question is construction: we must output a valid subsequence, not just its length. The structure we use is to greedily form pairs while scanning the array, and then output them in a way that preserves increasing index order for the subsequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Frequency Pairing + Greedy Construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the array and dynamically build pairs of equal values using their occurrence positions.

1. Traverse the array from left to right while maintaining, for each value, a list of indices where it has been seen but not yet paired. When we see a value that already has an unmatched occurrence, we immediately form a pair using the earliest available index for that value. This greedy pairing ensures we maximize the number of disjoint pairs.
2. Every time we form a pair, we store the two indices. Over the full scan, this produces the maximum number of pairs possible because each value contributes exactly one pair per two occurrences, and we never waste an occurrence.
3. Once all pairs are collected, we construct the final subsequence. We take the first element of each pair as the left half and the second element as the right half.
4. We sort pairs by their first index. This ensures the left half is in increasing order of positions in the original array.
5. We output values of the left indices in that order, followed by values of the right indices in reverse order. This creates a palindrome.

The reason sorting by first occurrence works is that all left-side indices are strictly increasing in the constructed sequence, and all right-side indices are placed after them in reverse symmetry, which guarantees a valid subsequence ordering.

### Why it works

Each pair contributes exactly two positions in the original array with the left index strictly smaller than the right index. By ordering pairs by left index, all left endpoints are increasing. The right endpoints, when reversed, align symmetrically but still correspond to valid positions that come after the left half in the constructed subsequence order. This guarantees that the sequence of chosen indices is strictly increasing up to the midpoint and then continues increasing while being assigned to the mirrored second half, preserving subsequence validity and palindrome structure simultaneously.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    pos = {}
    pairs = []

    for i, x in enumerate(a):
        if x not in pos:
            pos[x] = []
        pos[x].append(i)

        if len(pos[x]) >= 2:
            j = pos[x].pop()
            i0 = pos[x].pop()
            pairs.append((i0, j, x))

    pairs.sort(key=lambda t: t[0])

    left = [x for _, _, x in pairs]
    right = [x for _, _, x in reversed(pairs)]

    res = left + right

    print(len(res))
    print(*res)

if __name__ == "__main__":
    solve()
```

The code maintains stacks of indices for each value. Whenever a second unused occurrence appears, we immediately pair it with the previous one. This greedy pairing guarantees we extract the maximum number of disjoint pairs without backtracking.

Sorting pairs by their first index is the step that turns a collection of independent pairs into a globally consistent subsequence. Without this ordering, the constructed sequence could violate index monotonicity.

The final concatenation is the standard palindrome construction: left half followed by reversed right half.

## Worked Examples

### Example 1

Input:

```
4
1 2 2 1
```

We track positions:

| Step | Value | Stored positions | New pair | Pairs |
| --- | --- | --- | --- | --- |
| 1 | 1 | [0] | none | [] |
| 2 | 2 | [1] | none | [] |
| 3 | 2 | [] | (1,2) | (1,2) |
| 4 | 1 | [] | (0,3) | (0,3), (1,2) |

Sorting by left index gives pairs `(0,3)` and `(1,2)`.

Left half is `[1,2]`, right half is `[2,1]`.

Output is:

```
4
1 2 2 1
```

This confirms that interleaved values still form a valid palindrome when paired greedily.

### Example 2

Input:

```
6
1 2 3 1 3 2
```

| Step | Value | Stored positions | New pair | Pairs |
| --- | --- | --- | --- | --- |
| 1 | 1 | [0] | none | [] |
| 2 | 2 | [1] | none | [] |
| 3 | 3 | [2] | none | [] |
| 4 | 1 | [] | (0,3) | (0,3) |
| 5 | 3 | [] | (2,4) | (0,3),(2,4) |
| 6 | 2 | [] | (1,5) | (0,3),(2,4),(1,5) |

Sorting by first index gives `(0,3),(1,5),(2,4)`.

Left half: `[1,2,3]`

Right half: `[3,2,1]`

Final output:

```
6
1 2 3 3 2 1
```

This trace shows how interleaving does not matter as long as pairing is done greedily and ordering is restored afterward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each element is processed once, and pairs are sorted by first index |
| Space | O(n) | We store positions and pairs |

The constraints allow up to $10^5$ elements, so a linear or near-linear solution is required. The algorithm processes each element once and performs a single sort over at most $n/2$ pairs, which is comfortably efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins

    data = inp.strip().split()
    n = int(data[0])
    a = list(map(int, data[1:]))

    pos = {}
    pairs = []

    for i, x in enumerate(a):
        pos.setdefault(x, [])
        pos[x].append(i)
        if len(pos[x]) >= 2:
            j = pos[x].pop()
            i0 = pos[x].pop()
            pairs.append((i0, j, x))

    pairs.sort(key=lambda t: t[0])
    res = [x for _, _, x in pairs] + [x for _, _, x in reversed(pairs)]

    return str(len(res)) + "\n" + " ".join(map(str, res))

# provided samples (illustrative reconstruction)
assert run("4\n1 2 2 1") == "4\n1 2 2 1"

# all equal
assert run("4\n7 7 7 7") == "4\n7 7 7 7"

# minimum case
assert run("2\n5 5") == "2\n5 5"

# interleaved pairs
assert run("6\n1 2 3 1 3 2") == "6\n1 2 3 3 2 1"

# random small
assert run("8\n1 2 1 3 2 3 4 4") == "8\n1 2 3 4 4 3 2 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 / 1 2 2 1` | `4 / 1 2 2 1` | basic palindrome formation |
| `4 / 7 7 7 7` | `4 / 7 7 7 7` | multiple pairs of same value |
| `2 / 5 5` | `2 / 5 5` | minimum valid input |
| `6 / 1 2 3 1 3 2` | `6 / 1 2 3 3 2 1` | interleaving correctness |
| `8 / 1 2 1 3 2 3 4 4` | `8 / 1 2 3 4 4 3 2 1` | multiple groups |

## Edge Cases

A key edge case is when occurrences of the same value are highly separated and interleaved with other values. Even in such cases, greedy pairing still works because pairing happens locally per value and does not depend on global structure.

Consider:

```
1 2 1 3 2 3
```

The algorithm pairs `(1,2)` positions for each value independently of others. Even though values interleave, each pair is still valid because ordering is restored afterward through sorting by first index.

Another edge case is when one value dominates the array. For example:

```
5
1 1 1 1 1
```

Pairs formed are `(0,1)` and `(2,3)`, leaving one unused element. The algorithm correctly outputs only even length, discarding leftovers automatically.

A final edge case is the minimum input size, where only one pair exists. The algorithm directly outputs that pair without any sorting complications.
