---
title: "CF 103736B - New String"
description: "We are given a custom ordering of the English lowercase alphabet, where the 26 letters appear in a specific sequence that defines a strict total order. If a letter appears earlier in this ordering, it is considered smaller."
date: "2026-07-02T09:09:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103736
codeforces_index: "B"
codeforces_contest_name: "The 2022 Hangzhou Normal U Summer Trials"
rating: 0
weight: 103736
solve_time_s: 49
verified: true
draft: false
---

[CF 103736B - New String](https://codeforces.com/problemset/problem/103736/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a custom ordering of the English lowercase alphabet, where the 26 letters appear in a specific sequence that defines a strict total order. If a letter appears earlier in this ordering, it is considered smaller. This induces a lexicographic order on strings built from these letters.

After defining this custom alphabet order, we are given a collection of strings. The task is to determine which string would appear in position K if we sort all given strings using this custom lexicographic order, and then standard lexicographic comparison extended with length as a final tie-breaker.

The key point is that “lexicographically smallest” is not based on normal `'a' < 'b' < ... < 'z'`, but instead on the provided permutation of the alphabet.

From a computational perspective, n is at most 1000 and each string length is at most 1000. This makes an O(n log n) sort over string comparisons feasible, since each comparison is at worst O(1000). A brute-force enumeration of all permutations or constructing a full trie ranking structure would be unnecessary overkill.

A subtle edge case arises from the fact that the alphabet order is not standard. For example, if the order begins with `zabcdefghijklmnopqrstuvwxy`, then `'z'` is smallest and `'a'` is second smallest. A naive implementation that forgets to remap characters would produce a completely incorrect ordering while still passing many accidental tests.

Another potential pitfall is misunderstanding lexicographic comparison rules. The comparison is prefix-sensitive: if one string is a prefix of another, the shorter string is smaller. For instance, if `"a"` and `"ab"` are compared, `"a"` must come first regardless of alphabet order.

## Approaches

The brute-force approach would be to define a comparator that directly compares two strings character by character using the given alphabet ordering, and then sort the entire array. This is correct because lexicographic ordering is fully determined by pairwise comparisons. However, this approach still depends on repeated comparisons of strings, and each comparison can scan up to O(L) characters where L is the maximum string length. With n up to 1000 and L up to 1000, sorting yields roughly O(n log n · L), which is around 10^7 character checks in the worst case, still acceptable in Python.

A more structured observation is that the only difficulty lies in comparing characters efficiently. Once we convert each character into its rank in the custom alphabet, every string becomes a sequence of integers, and standard lexicographic ordering applies directly. This removes the overhead of repeated dictionary lookups inside comparisons and makes the sort cleaner and faster in practice.

Thus the optimal solution is simply to build a mapping from character to rank and sort using transformed keys.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Comparator | O(n log n · L) | O(1) extra | Accepted |
| Rank Mapping + Key Sort | O(n · L log n) | O(26 + nL) | Accepted |

## Algorithm Walkthrough

1. Read the custom alphabet order string and construct an array `rank` such that `rank[c]` gives the position of character `c` in this order. This allows O(1) comparison between any two characters. The reason this is necessary is that direct string comparison depends on repeated lookups into a nonstandard order.
2. Read all input strings into a list. Each string will later be converted into a comparable representation under the custom ordering.
3. For each string, construct a transformed version where every character is replaced by its rank value. This transforms lexicographic comparison under a custom alphabet into normal lexicographic comparison over integers. This step is conceptually a normalization of the problem.
4. Sort the list of strings using these transformed representations as the sorting key. Python’s built-in sort will then correctly apply lexicographic ordering on tuples or lists of integers.
5. Output the K-th string from the original list after sorting. We keep original strings alongside their transformed keys so we do not lose the actual output format.

### Why it works

The transformation preserves ordering because the lexicographic comparison rule depends only on the relative order of characters, not their actual identities. By mapping each character to its rank in the custom alphabet, we embed the custom order into standard integer order. Since Python compares sequences lexicographically, comparing transformed arrays is equivalent to comparing original strings under the given alphabet.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    order = input().strip()
    rank = [0] * 26
    for i, ch in enumerate(order):
        rank[ord(ch) - 97] = i

    n = int(input())
    arr = []
    for _ in range(n):
        s = input().strip()
        key = tuple(rank[ord(c) - 97] for c in s)
        arr.append((key, s))

    k = int(input())
    arr.sort(key=lambda x: x[0])
    print(arr[k - 1][1])

if __name__ == "__main__":
    solve()
```

The implementation first builds a direct mapping from characters to their custom order indices. This avoids repeated scanning of the alphabet string during comparisons.

Each string is paired with a tuple representation of its characters under the new ordering. A tuple is used because Python compares tuples lexicographically in O(length of tuple), which aligns exactly with the intended string comparison behavior.

Sorting is done using these keys, and we extract the K-th element after sorting.

A common subtle mistake would be forgetting to convert characters into ranks and instead relying on ASCII ordering, which would completely invalidate the result whenever the custom alphabet differs from standard order.

## Worked Examples

### Example 1

Input:

```
acbdefghijklmnopqrstuvwxyz
abc
acb
2
```

Custom order means `'a' < 'c' < 'b' < ...`.

| String | Transformed Key |
| --- | --- |
| abc | (0, 2, 1) |
| acb | (0, 1, 2) |

Sorted order becomes:

`acb`, `abc`

For K = 2, output is `abc`.

This demonstrates how swapping just two characters in the alphabet completely reverses comparisons between strings that share those characters.

### Example 2

Input:

```
zabcdefghijklmnopqrstuvwxy
a
b
1
```

Here `'z'` is smallest, then `'a'`, then `'b'`.

| String | Key |
| --- | --- |
| a | (1,) |
| b | (2,) |

Sorted order is `a`, `b`. For K = 1, output is `a`.

This confirms prefix-free single-character comparison under a nonstandard alphabet behaves exactly like integer comparison after mapping.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n · L) | Sorting n strings with length L using lexicographic tuple comparisons |
| Space | O(nL) | Storage of transformed keys for all strings |

Given n ≤ 1000 and L ≤ 1000, this comfortably fits within limits. The dominant factor is sorting, but the constants are small and Python handles tuple comparison efficiently.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like case
assert run("""acbdefghijklmnopqrstuvwxyz
3
abc
acb
bca
2
""") == "abc"

# already sorted case
assert run("""abcdefghijklmnopqrstuvwxyz
3
a
aa
b
1
""") == "a"

# reverse alphabet
assert run("""zyxwvutsrqponmlkjihgfedcba
3
a
b
c
3
""") == "a"

# identical prefixes
assert run("""abcdefghijklmnopqrstuvwxyz
4
abc
ab
abcd
a
3
""") == "abc"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mixed alphabet order | abc | custom ordering correctness |
| natural alphabet | a | standard lexicographic fallback |
| reversed alphabet | a | full inversion handling |
| prefix-heavy set | abc | prefix comparison rule |

## Edge Cases

A key edge case is when strings are identical except for characters whose order is nontrivial in the custom alphabet. For instance, with ordering `acb...`, comparing `"ab"` and `"ac"` depends entirely on the relative order of `b` and `c`. The algorithm handles this correctly because both characters are converted into ranks before comparison.

Another edge case is prefix relationships. Consider `"ab"` and `"a"`. Even if `b` is smaller than most characters in the alphabet, `"a"` must still come first because the comparison terminates at the end of the shorter string. The tuple representation preserves this automatically since `(rank('a'),)` is shorter than `(rank('a'), rank('b'))`, and Python’s lexicographic tuple comparison treats the shorter prefix as smaller.

Finally, cases with maximum length strings are handled safely because the transformation is linear per string and does not modify structure beyond conversion, ensuring no hidden recursion or deep copying overhead appears.
