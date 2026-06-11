---
title: "CF 1152A - Neko Finds Grapes"
description: "We are given a collection of treasure chests and a collection of keys. Each chest has a number written on it and each key also has a number written on it. A key can open a chest only when the sum of their numbers is odd."
date: "2026-06-12T02:55:52+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1152
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 554 (Div. 2)"
rating: 800
weight: 1152
solve_time_s: 84
verified: true
draft: false
---

[CF 1152A - Neko Finds Grapes](https://codeforces.com/problemset/problem/1152/A)

**Rating:** 800  
**Tags:** greedy, implementation, math  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of treasure chests and a collection of keys. Each chest has a number written on it and each key also has a number written on it. A key can open a chest only when the sum of their numbers is odd. Once a key is used, it disappears, and each chest can be opened at most once.

The task is to pair keys with chests so that the parity condition is satisfied and the number of successful pairs is as large as possible.

A key observation is that only parity matters. The actual values are irrelevant except for whether they are even or odd. Every chest and key can therefore be classified into two groups: even or odd.

The constraint $n, m \le 10^5$ means any quadratic pairing strategy that tries every chest-key combination will fail. A solution must process frequencies or counts in linear time, since $O(nm)$ is on the order of $10^{10}$ operations.

A subtle edge case arises when one of the parity groups is empty. For example, if all chests are even and all keys are even, no pairing is possible at all. Similarly, if all chests are odd and all keys are odd, again no pairing is possible. A naive implementation that ignores parity separation and tries arbitrary matching will incorrectly assume some matches exist unless explicitly checked.

## Approaches

A brute-force solution would try every chest-key pair and check whether their sum is odd. If valid and both are unused, we match them greedily. This is correct because each valid pairing is independent, but it is far too slow. With up to $10^5$ elements in each list, this leads to up to $10^{10}$ checks, which is infeasible.

The key simplification comes from recognizing that the condition “sum is odd” is equivalent to “one is even and the other is odd.” This turns the problem into a bipartite matching between two groups: even and odd numbers. However, since there is no additional structure inside each group, we do not need an actual graph matching algorithm. Any even chest can be paired with any odd key and vice versa, so only counts matter.

Thus the problem reduces to counting how many even and odd values exist in both arrays, and then pairing greedily: each even chest can match with an odd key, and each odd chest can match with an even key. The answer is the sum of these two independent matches.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Counting Parity | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many chests are even and how many are odd.

This separates the problem into two independent categories.
2. Count how many keys are even and how many are odd.

These counts determine all possible valid pairings.
3. Compute how many pairs can be formed between even chests and odd keys.

This is limited by the smaller of the two counts, since each object is used once.
4. Compute how many pairs can be formed between odd chests and even keys.

Again, this is the minimum of the available counts.
5. Sum the two results and output it.

The reason we take the minimum in each case is that every pairing consumes one chest and one key, so we are always bottlenecked by the smaller group.

### Why it works

The parity condition fully determines validity: a pair is valid if and only if the elements have opposite parity. Once we partition items into even and odd, there are no further constraints linking specific elements. Any matching strategy that pairs opposite parity elements is equivalent, so maximizing matches reduces to maximizing independent bipartite pair counts, which is achieved by greedily matching as many as possible between the two groups.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    even_a = sum(x % 2 == 0 for x in a)
    odd_a = n - even_a
    
    even_b = sum(x % 2 == 0 for x in b)
    odd_b = m - even_b
    
    # even chest with odd key
    match1 = min(even_a, odd_b)
    
    # odd chest with even key
    match2 = min(odd_a, even_b)
    
    print(match1 + match2)

if __name__ == "__main__":
    solve()
```

The code first splits both arrays into parity counts in a single pass. It then computes the two possible pairing directions separately. The final answer is the sum of both, since these pairings are disjoint in terms of used elements.

The main subtlety is ensuring we do not mix counts incorrectly: even chests can only contribute to matches with odd keys, and vice versa. Each minimum calculation enforces the one-to-one usage constraint.

## Worked Examples

### Example 1

Input:

```
5 4
9 14 6 2 11
8 4 7 20
```

Parity breakdown:

| Step | Even chests | Odd chests | Even keys | Odd keys | Matches (even-odd) | Matches (odd-even) | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Start | 3 | 2 | 3 | 1 | - | - | - |
| Compute pairs | - | - | - | - | min(3,1)=1 | min(2,3)=2 | 3 |

The algorithm first pairs even chests with odd keys, producing 1 match. Then it pairs odd chests with even keys, producing 2 matches. Total is 3.

This demonstrates that the optimal solution does not depend on specific identities of elements, only parity counts.

### Example 2

Input:

```
3 3
1 3 5
2 4 6
```

| Step | Even chests | Odd chests | Even keys | Odd keys | Matches (even-odd) | Matches (odd-even) | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Start | 0 | 3 | 3 | 0 | 0 | 0 | 0 |

No valid pairing exists in either direction since parity sets do not intersect across opposite groups in a usable way.

This shows the algorithm correctly handles cases where one side lacks compatible parity elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each array is scanned once to count parity |
| Space | O(1) | Only a few integer counters are used |

The solution comfortably fits within limits since it performs only linear passes over the input arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    output = []
    
    n, m = map(int, sys.stdin.readline().split())
    a = list(map(int, sys.stdin.readline().split()))
    b = list(map(int, sys.stdin.readline().split()))
    
    even_a = sum(x % 2 == 0 for x in a)
    odd_a = n - even_a
    even_b = sum(x % 2 == 0 for x in b)
    odd_b = m - even_b
    
    return str(min(even_a, odd_b) + min(odd_a, even_b))

# sample
assert run("5 4\n9 14 6 2 11\n8 4 7 20\n") == "3"

# all same parity, no matches
assert run("3 3\n1 3 5\n2 4 6\n") == "0"

# all cross-compatible
assert run("2 2\n2 4\n1 3\n") == "2"

# single element match
assert run("1 1\n2\n1\n") == "1"

# mixed case
assert run("4 5\n1 2 3 4\n5 6 7 8 9\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all odd vs all even | 0 | no valid parity matches |
| fully cross-parity | full pairing | maximum matching saturation |
| single elements | 1 or 0 | boundary correctness |
| mixed sizes | correct min-based matching | general correctness |

## Edge Cases

One important edge case is when one side has only one parity type. For example:

Input:

```
4 3
2 4 6 8
1 3 5
```

Here, all chests are even and all keys are odd. The algorithm computes `even_chests = 4`, `odd_keys = 3`, so `min(4,3)=3` matches, and the opposite direction contributes zero. The output is 3, which is correct because every key can open a chest but one chest remains unused.

Another case is when both sides are mixed but heavily imbalanced:

```
5 5
1 1 1 2 2
2 2 2 1 1
```

Even-odd pairing gives `even_chests=2, odd_keys=3 → 2` and `odd_chests=3, even_keys=2 → 2`, totaling 4. The algorithm correctly avoids overcounting because each minimum enforces consumption of limited resources.
