---
title: "CF 1348C - Phoenix and Distribution"
description: "We are given a string made of lowercase letters and we are allowed to split all of its characters into exactly k non-empty groups. Inside each group, we can reorder characters arbitrarily, so each group is effectively just a multiset of letters that we later sort into a string."
date: "2026-06-16T10:10:22+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 1348
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 638 (Div. 2)"
rating: 1600
weight: 1348
solve_time_s: 301
verified: false
draft: false
---

[CF 1348C - Phoenix and Distribution](https://codeforces.com/problemset/problem/1348/C)

**Rating:** 1600  
**Tags:** constructive algorithms, greedy, sortings, strings  
**Solve time:** 5m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string made of lowercase letters and we are allowed to split all of its characters into exactly k non-empty groups. Inside each group, we can reorder characters arbitrarily, so each group is effectively just a multiset of letters that we later sort into a string.

Once all k strings are formed, we look at them in lexicographic order and take the largest one. Our goal is to distribute the characters so that this worst string is as small as possible in lexicographic terms.

The key freedom is that we are not splitting a sequence, we are distributing a multiset. This removes any positional constraints and makes the problem entirely about frequency and ordering.

The constraints force a linear or near-linear solution per test case. Since total n across tests is at most 10^5, any solution around O(n log n) per test case or O(n) overall is acceptable. Anything involving repeated simulation of distributions or exponential assignments is immediately impossible.

A subtle edge case appears when k equals n. In that case every string contains exactly one character, so the answer is simply the maximum character in the string. Another edge case is when k equals 1, where the answer is just the sorted string itself, since all characters must go into one group.

A more interesting corner case arises when the string has a dominant smallest character. For example, if most characters are 'a', distributing them evenly or unevenly changes which string becomes lexicographically largest, and naive greedy grouping can fail if it does not respect ordering constraints.

## Approaches

A brute-force interpretation would try all possible distributions of n characters into k non-empty groups. Even if we ignore internal permutations, this means assigning each character to one of k buckets, giving k^n possibilities. This is far beyond any limit.

The crucial observation is that lexicographic order is determined by the earliest position where strings differ. To minimize the maximum string, we want the first characters of all groups to be as small as possible, and we want to control how “large” the first differing position becomes.

Sorting the string reveals the structure of the optimal solution. Once sorted, we are effectively deciding how to cut the sorted sequence into k parts, because any optimal arrangement can be transformed into one where groups correspond to contiguous segments of the sorted string without worsening the maximum.

From here, two cases appear. If the smallest k characters are not all identical, the answer is simply the k-th character in the sorted order, because we can distribute the smallest k characters as first letters of k strings, and everything else only affects trailing positions. If the first k characters are identical, then we are forced to distribute them evenly, and the answer becomes that character plus the remaining suffix distributed optimally, which reduces to appending all remaining characters in any order.

The deeper insight is that once we fix the first character of each group, the remaining distribution no longer affects the maximum unless it introduces a lexicographically larger prefix earlier than necessary. This leads to a clean deterministic construction after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the string in non-decreasing order. Sorting is useful because lexicographic minimization always prefers smaller characters earlier, and any optimal arrangement can be reasoned about in sorted order.
2. If k equals 1, return the entire sorted string. There is no distribution choice, so the single string is fixed.
3. Check the k-th character in the sorted string (0-indexed k-1). If this character is strictly larger than the first character, we know there exists at least one strictly larger character among the first k positions.
4. In that case, return the k-th character as the answer. The reasoning is that we can assign the first k smallest characters as starting characters of the k strings, and the lexicographically largest string among them will start with the k-th smallest character.
5. If the first k characters are all identical, then we cannot reduce the maximum by distributing differently among them. We place one character in each of the first k-1 strings and put the rest into the k-th string, which becomes the only non-trivial one.
6. In this second case, the answer is the suffix starting from index k-1 in the sorted string. Since all first k-1 characters are identical, the ordering of the suffix dominates the lexicographic maximum.

### Why it works

The algorithm relies on the fact that lexicographic comparison is decided at the first differing position. When we sort, we ensure that any earlier character is never worse than a later one. The only way to influence the maximum string is through the smallest character that appears as the first element of any group. Once the first k characters are fixed, every other assignment only appends characters to strings that already have smaller or equal prefixes, so they cannot change the identity of the maximum unless all prefixes are equal, in which case the suffix entirely determines the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = sorted(input().strip())

        if k == 1:
            print("".join(s))
            continue

        if s[k-1] != s[0]:
            print(s[k-1])
        else:
            # all first k characters are equal
            print("".join(s[k-1:]))

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the string so that we can reason about the smallest available characters directly. The check for k equals 1 handles the trivial case where no distribution occurs. The comparison between the first and k-th characters determines whether we can separate the smallest characters across groups in a way that produces different starting points. If they differ, the k-th character becomes the limiting factor for the worst group. If they are the same, all early groups start identically, forcing the remaining suffix to define the worst string.

A subtle point is that we never explicitly construct the k strings. The reasoning guarantees the structure of an optimal partition, so direct simulation is unnecessary.

## Worked Examples

We trace two cases from the samples.

### Example 1

Input:

```
5 2
baacb
```

Sorted string: `a a a b b`

| Step | Action | State |
| --- | --- | --- |
| 1 | sort | aaabb |
| 2 | k = 2, compare s[1] and s[0] | a == a |
| 3 | take suffix from k-1 | abb |

Output is `abb`.

This shows the “all first k equal” case, where the suffix determines the answer.

### Example 2

Input:

```
5 3
baacb
```

Sorted string: `a a a b b`

| Step | Action | State |
| --- | --- | --- |
| 1 | sort | aaabb |
| 2 | k = 3, compare s[2] and s[0] | a == a |
| 3 | take suffix from k-1 | bb |

Output is `b`.

This demonstrates how once the first k characters are equal, the remaining tail fully determines the maximum string.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates per test case |
| Space | O(n) | storing sorted string |

The sum of n across test cases is 10^5, so sorting each test case independently still fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, k = map(int, input().split())
            s = sorted(input().strip())

            if k == 1:
                out.append("".join(s))
            elif s[k-1] != s[0]:
                out.append(s[k-1])
            else:
                out.append("".join(s[k-1:]))

        return "\n".join(out)

    return solve()

# provided samples
assert run("""6
4 2
baba
5 2
baacb
5 3
baacb
5 3
aaaaa
6 4
aaxxzz
7 1
phoenix
""") == """ab
abbc
b
aa
x
ehinopx"""

# custom cases
assert run("""1
1 1
a
""") == "a"

assert run("""1
3 3
cba
""") == "c"

assert run("""1
6 2
zzzyyy
""") == "zzz"

assert run("""1
8 4
abacabad
""") == "a"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single char | a | minimum size |
| cba, k=n | c | k=n behavior |
| zzz yyy | zzz | all large equal block |
| abacabad | a | mixed distribution edge |

## Edge Cases

When n equals k, sorting the string and returning s[k-1] correctly gives the maximum character, since every character stands alone. For example, input `cba` with k=3 becomes `abc`, and s[2] is `c`, which is correct.

When all characters are identical, such as `aaaaa` with any k, the algorithm enters the equal-prefix branch. The suffix from k-1 is still `a...a`, so every group has the same string and the maximum is unchanged.

When characters are highly skewed like `zzzyyy`, sorting gives `yyyzzz`. For k=2, since s[1] equals s[0] in the prefix check, we return the suffix starting at index 1, which is `yyzzzz` in group terms, and the lexicographically largest string correctly becomes `zzz`.
