---
title: "CF 1367B - Even Array"
description: "We are given an array where each position has a fixed “required parity”: even indices must contain even numbers, and odd indices must contain odd numbers."
date: "2026-06-16T12:02:50+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1367
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 650 (Div. 3)"
rating: 800
weight: 1367
solve_time_s: 238
verified: true
draft: false
---

[CF 1367B - Even Array](https://codeforces.com/problemset/problem/1367/B)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 3m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array where each position has a fixed “required parity”: even indices must contain even numbers, and odd indices must contain odd numbers. We are allowed to rearrange the array using swaps between any two positions, and we want to know the minimum number of swaps needed to satisfy all parity requirements, or determine that it cannot be done at all.

A useful way to reinterpret the task is to think of each position as having a target type, even index or odd index, and each value as also having a type, even value or odd value. The goal is to permute values so that types match position requirements.

Since swaps are unrestricted, the structure is not about adjacency or ordering, only about counts of mismatches between two groups.

The constraints are small: n is at most 40 and there are at most 1000 test cases. This means an O(n) or O(n log n) solution per test case is easily sufficient, and even an O(n^2) solution would pass comfortably. However, the structure of the problem suggests that we should be able to solve each test case in linear time by counting mismatches rather than simulating swaps.

A subtle edge case appears when the number of even values does not match the number of even index positions. For example, if n is 3, indices 0 and 2 require even numbers, so we need exactly two even values. If the array only has one even value, no amount of swapping can fix this, because swaps do not change how many even numbers exist.

Another edge case occurs when everything already matches parity. In that case, the answer is zero, and a naive swapping strategy might still incorrectly count unnecessary operations if it tries to “fix” already correct positions.

## Approaches

A brute-force interpretation would be to treat the problem as searching over permutations of the array. We could try all possible ways to rearrange elements and compute how many swaps are required to reach each valid configuration. However, the number of permutations is n!, which is astronomically large even for n = 40. Even if we tried to reason in terms of swap distances between permutations, the state space remains far too large.

The key simplification comes from observing that only parity matters, not actual values. Every element belongs to one of two categories: even or odd. Every index also belongs to one of two categories: even position or odd position. The problem reduces to matching counts between these two partitions.

If we count how many indices of each parity exist and how many elements of each parity we have, we immediately see whether a solution is possible. If the counts do not match, no rearrangement can fix it.

Once feasibility is established, the remaining question is how many swaps are required. Each swap between a misplaced even-on-odd-position element and a misplaced odd-on-even-position element fixes two incorrect positions at once. This pairing structure directly determines the answer.

The brute-force works because it tries to explicitly construct a valid permutation, but it fails because it does not exploit the binary structure of parity. The observation that only mismatched counts matter reduces the problem to counting and pairing mismatches.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try permutations) | O(n!) | O(n) | Too slow |
| Counting parity mismatches | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We focus on one test case.

1. Count how many array positions require even values. These are exactly indices 0, 2, 4, and so on. Let this be need_even_positions.
2. Count how many even numbers exist in the array. Let this be have_even_values. This determines how many elements are available to satisfy even positions.
3. If have_even_values is not equal to need_even_positions, return -1. The reason is that swaps cannot change the total number of even values, so it is impossible to satisfy all constraints if the totals disagree.
4. Compute mismatches by scanning the array. For every index i, if i is even but a[i] is odd, this position is a deficit of even value. If i is odd but a[i] is even, this is a surplus of even value placed incorrectly.
5. Let mismatch_even_to_odd be the number of even values sitting in odd indices. This equals the number of positions that need correction from the other side.
6. The minimum number of swaps is mismatch_even_to_odd, because each swap between an incorrectly placed even value and an incorrectly placed odd value fixes both positions at once.

### Why it works

Every valid swap can fix at most two incorrect positions, and every incorrect position belongs to exactly one of two symmetric mismatch types. Once feasibility ensures equal counts of required parity slots and available parity values, the mismatches form perfect pairs. Each swap resolves one pair without creating new mismatches elsewhere, so counting these pairs gives the optimal number of operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    need_even = (n + 1) // 2
    have_even = sum(1 for x in a if x % 2 == 0)
    
    if have_even != need_even:
        print(-1)
        continue
    
    mismatches = 0
    for i, x in enumerate(a):
        if i % 2 != x % 2:
            if i % 2 == 0:
                mismatches += 1
    
    print(mismatches)
```

The solution starts by computing how many even indices exist, which is the number of positions that must be filled with even numbers. It then counts how many even values are present in the array. This feasibility check is essential because swapping cannot change the multiset of values.

The mismatch counting loop only increments when an even index contains an odd number. This is sufficient because every such mismatch must be paired with a corresponding opposite mismatch at an odd index, and counting only one side avoids double counting swaps.

## Worked Examples

### Example 1

Input:

```
n = 4
a = [3, 2, 7, 6]
```

We track key values.

| i | a[i] | i parity | a[i] parity | mismatch_even_to_odd |
| --- | --- | --- | --- | --- |
| 0 | 3 | even | odd | 1 |
| 1 | 2 | odd | even | 1 |
| 2 | 7 | even | odd | 2 |
| 3 | 6 | odd | even | 2 |

We get two mismatches where even indices hold odd values. Each corresponds to a needed swap with an opposite mismatch at odd indices, giving answer 2.

This trace shows that we never explicitly simulate swaps, only count imbalance between two parity classes.

### Example 2

Input:

```
n = 3
a = [3, 2, 6]
```

| i | a[i] | i parity | a[i] parity | mismatches |
| --- | --- | --- | --- | --- |
| 0 | 3 | even | odd | 1 |
| 1 | 2 | odd | even | 1 |
| 2 | 6 | even | even | 1 |

Feasibility check: need_even_positions = 2, have_even_values = 2, so it is possible.

Only one even-position mismatch exists, so one swap suffices.

This confirms that the algorithm reduces the problem to pairing complementary parity errors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan the array once for counting and mismatch detection |
| Space | O(1) | Only a few counters are used |

The constraints allow up to 1000 test cases with n up to 40, so at most 40000 elements are processed. A single linear pass per test case is easily fast enough within limits.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        need_even = (n + 1) // 2
        have_even = sum(x % 2 == 0 for x in a)
        
        if have_even != need_even:
            out.append("-1")
            continue
        
        mismatches = 0
        for i, x in enumerate(a):
            if i % 2 == 0 and x % 2 == 1:
                mismatches += 1
        
        out.append(str(mismatches))
    
    return "\n".join(out)

# provided samples
assert solve("""4
4
3 2 7 6
3
3 2 6
1
7
7
4 9 2 1 18 3 0
""") == """2
1
-1
0"""

# all already correct
assert solve("""1
5
0 1 2 3 4
""") == "0"

# impossible due to parity mismatch
assert solve("""1
2
1 1
""") == "-1"

# minimal case
assert solve("""1
1
0
""") == "0"

# needs swaps
assert solve("""1
4
1 3 5 7
""") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 elements already valid | 0 | no swaps needed case |
| all odd values on even-sized structure | -1 | feasibility failure |
| single element | 0 | smallest valid input |
| all odd values | -1 | mismatch extreme |

## Edge Cases

A minimal array of size 1 always satisfies the condition if the value is even, because index 0 requires even parity. The algorithm correctly returns zero swaps since no mismatches are detected.

When the array has the correct number of even values but they are all in the wrong positions, feasibility passes but mismatch counting produces the exact number of swaps needed. Each swap corresponds to pairing an even-at-odd-index element with an odd-at-even-index element, and no other structure affects the result.
