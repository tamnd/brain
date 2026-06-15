---
title: "CF 1216A - Prefixes"
description: "We are given a binary string made only of the characters a and b, and its length is guaranteed to be even. The task is to transform this string using the minimum number of single-character flips so that every prefix whose length is even contains exactly the same number of a and…"
date: "2026-06-15T18:43:12+07:00"
tags: ["codeforces", "competitive-programming", "strings"]
categories: ["algorithms"]
codeforces_contest: 1216
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 587 (Div. 3)"
rating: 800
weight: 1216
solve_time_s: 158
verified: false
draft: false
---

[CF 1216A - Prefixes](https://codeforces.com/problemset/problem/1216/A)

**Rating:** 800  
**Tags:** strings  
**Solve time:** 2m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string made only of the characters `a` and `b`, and its length is guaranteed to be even. The task is to transform this string using the minimum number of single-character flips so that every prefix whose length is even contains exactly the same number of `a` and `b`.

A useful way to rephrase the requirement is to scan the string from left to right and look at prefixes of length 2, 4, 6, and so on. Each such prefix must be perfectly balanced, meaning half of its characters are `a` and the other half are `b`.

The key constraint is that we are allowed to flip any position independently, turning `a` into `b` or vice versa, and we want to minimize how many flips are needed.

Since the string length can be up to 200,000, any solution must run in linear time. Anything that repeatedly recomputes prefix statistics or tries combinations of modifications per prefix will be too slow. This strongly suggests that each position should be processed at most once or twice in a greedy or constructive manner.

A subtle edge case arises when local decisions affect earlier prefixes. For example, a naive idea might be to fix each prefix independently, but that would re-break earlier prefixes. Another mistake is trying to globally count how many `a` and `b` are needed, without respecting the prefix-by-prefix constraint, which ignores the fact that each prefix imposes its own balance requirement progressively.

For instance, if we had `bbbb`, a naive global view says we need two `a` and two `b`, but does not immediately explain where to place them. The correct answer depends on enforcing balance at every even prefix step, not just at the end.

## Approaches

A brute-force approach would attempt to enforce the condition prefix by prefix. For every even length prefix, we could check whether it is balanced, and if not, try all possible flips of characters inside it to fix the imbalance. This quickly becomes exponential because fixing one prefix may require exploring many combinations of flips, and each prefix depends on previous modifications. Even a greedy recomputation per prefix would cost O(n) per prefix, leading to O(n²) overall.

The key observation is that prefixes are not independent. When we move from prefix of length `i-2` to prefix of length `i`, only two new characters are introduced. This means we can maintain a running imbalance condition locally.

We can interpret the problem as constructing a target string that satisfies a very simple structural constraint: every pair `(1,2)`, `(3,4)`, `(5,6)`, and so on, must form one `a` and one `b` in some order. Each pair is independent of all others because balancing is checked only at even boundaries, not at odd positions. This decouples the problem into independent decisions per pair.

For each pair, we choose the arrangement (`ab` or `ba`) that minimizes flips compared to the original characters. Summing these minimal local costs gives the global optimum.

This works because any valid final string must satisfy the constraint that every two consecutive positions contain exactly one `a` and one `b`, and any deviation inside a pair affects only that pair’s cost.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the string in chunks of two characters.

1. Split the string into pairs `(s[0], s[1]), (s[2], s[3]), ...`. Each pair must become one `a` and one `b`. This follows directly from the requirement that every even prefix is balanced.
2. For each pair, compute the cost of converting it into `"ab"`, which is the number of mismatches between the current pair and `"ab"`.
3. Also compute the cost of converting the same pair into `"ba"`.
4. Choose the cheaper of the two options for that pair. If costs are equal, either choice is valid.
5. Apply the chosen transformation to construct the final string.
6. Sum all chosen costs to obtain the minimum number of operations.

### Why it works

Each even prefix ending at position `2k` consists exactly of the first `k` pairs. The balance condition for that prefix is satisfied if and only if each pair contains exactly one `a` and one `b`. There is no cross-pair interaction in the constraint, so optimizing each pair independently cannot harm other pairs. This creates a decomposition of the global optimization problem into independent local minimizations, which guarantees optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
s = list(input().strip())

ans = 0
res = []

for i in range(0, n, 2):
    a, b = s[i], s[i + 1]

    # cost to make "ab"
    cost_ab = (a != 'a') + (b != 'b')
    # cost to make "ba"
    cost_ba = (a != 'b') + (b != 'a')

    if cost_ab <= cost_ba:
        ans += cost_ab
        res.append('a')
        res.append('b')
    else:
        ans += cost_ba
        res.append('b')
        res.append('a')

print(ans)
print("".join(res))
```

The solution reads the string and processes it two characters at a time. For each pair, it evaluates both possible valid configurations and selects the one requiring fewer flips. The result string is constructed incrementally, ensuring consistency with the chosen minimal-cost structure. The answer counter tracks how many flips were required across all pairs.

A common subtlety here is ensuring that we never attempt to enforce prefix balance globally. The correctness relies entirely on the decomposition into independent pairs.

## Worked Examples

### Example 1

Input:

```
4
bbbb
```

We process pairs: `(b,b)` and `(b,b)`.

| Pair | Option | Cost | Chosen |
| --- | --- | --- | --- |
| bb | ab | 2 |  |
| bb | ba | 2 | either |
| bb | ab | 2 |  |
| bb | ba | 2 | either |

We choose `ab` for first pair and `ba` for second pair.

Final string becomes `abba`, with total cost `2`.

This confirms that even when all characters are identical, local pairing still produces a balanced construction.

### Example 2

Input:

```
6
ababab
```

Pairs: `(a,b)`, `(a,b)`, `(a,b)`.

| Pair | Option | Cost | Chosen |
| --- | --- | --- | --- |
| ab | ab | 0 | keep |
| ab | ba | 2 |  |
| ab | ab | 0 | keep |

All pairs already match `ab`, so no flips are needed. The output remains unchanged.

This shows the algorithm correctly identifies already valid structures without unnecessary modifications.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each pair of characters is processed once with constant work |
| Space | O(n) | We construct the resulting string |

The linear complexity is sufficient for `n ≤ 2 × 10^5`, and the memory usage is dominated by storing the output string, which is also linear.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    n = int(input().strip())
    s = list(input().strip())

    ans = 0
    res = []

    for i in range(0, n, 2):
        a, b = s[i], s[i + 1]

        cost_ab = (a != 'a') + (b != 'b')
        cost_ba = (a != 'b') + (b != 'a')

        if cost_ab <= cost_ba:
            ans += cost_ab
            res.append('a')
            res.append('b')
        else:
            ans += cost_ba
            res.append('b')
            res.append('a')

    print(ans)
    print("".join(res))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("4\nbbbb\n") == "2\nabba"
assert run("4\nabba\n") == "0\nabba"

# custom cases
assert run("2\naa\n") == "1\nab"
assert run("2\nbb\n") == "1\nab"
assert run("2\nab\n") == "0\nab"
assert run("6\nbbbbbb\n") == "3\nababab"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 aa` | `1 ab` | minimal single-pair correction |
| `2 bb` | `1 ab` | symmetry with opposite characters |
| `2 ab` | `0 ab` | already valid pair |
| `6 bbbbbb` | `3 ababab` | repeated worst-case structure |

## Edge Cases

A key edge case is when both characters in a pair are identical, such as `"aa"` or `"bb"`. In these situations, both valid target configurations (`ab` and `ba`) have the same cost, and choosing either does not affect other pairs. The algorithm correctly handles this because it compares both options independently per pair and allows ties.

For input:

```
4
aaaa
```

Processing:

First pair `"aa"` becomes `"ab"` (cost 1), second pair `"aa"` becomes `"ab"` (cost 1). Total cost is 2.

Trace:

| i | pair | cost_ab | cost_ba | chosen |
| --- | --- | --- | --- | --- |
| 0 | aa | 1 | 1 | ab |
| 2 | aa | 1 | 1 | ab |

Final output `abab` satisfies both even-prefix constraints:

`ab` is balanced, and `abab` is also balanced.

This confirms that local greedy decisions per pair are sufficient even when the entire string is uniform.
