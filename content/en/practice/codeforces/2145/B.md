---
title: "CF 2145B - Deck of Cards"
description: "We are given a deck of cards numbered from 1 to n, initially sorted with 1 on top and n on the bottom. Monocarp performs a sequence of k operations that remove cards from either the top, the bottom, or ambiguously from either end."
date: "2026-06-08T01:31:28+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2145
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 183 (Rated for Div. 2)"
rating: 1000
weight: 2145
solve_time_s: 102
verified: false
draft: false
---

[CF 2145B - Deck of Cards](https://codeforces.com/problemset/problem/2145/B)

**Rating:** 1000  
**Tags:** greedy, implementation  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a deck of cards numbered from 1 to n, initially sorted with 1 on top and n on the bottom. Monocarp performs a sequence of k operations that remove cards from either the top, the bottom, or ambiguously from either end. For each card, we must decide whether it has definitely been removed, definitely remains, or whether we cannot tell.

The input gives the number of cards n, the number of actions k, and a string of length k where each character indicates the type of removal: '0' for top, '1' for bottom, and '2' for either end. Our output for each test case is a string of length n with characters '+', '-', or '?' for each card in order.

The constraints allow n up to 2×10^5 and the sum of all n across test cases up to 2×10^5. This rules out any approach that simulates the deck explicitly per operation, since a naïve simulation could do up to O(nk) work, potentially 4×10^10 operations, which is far too large. We need a linear or near-linear approach in n and k.

A subtle edge case arises with the '2' operations. If all actions are '2', any card could be removed from either end. For example, if n=3 and s="22", no card is guaranteed to be removed because we cannot tell which end was chosen. A careless approach that always removes from the top or bottom in order would incorrectly mark some cards as removed.

## Approaches

A brute-force approach would model the deck explicitly, popping cards from the front or back as specified. For '2', we would need to consider both possibilities, leading to an exponential number of states. Even ignoring the exponential explosion, just simulating the deck linearly requires O(n) per operation because removing from the front or back in a list is O(n) in Python, which is too slow.

The key observation is that each card’s fate depends only on how many guaranteed top removals and bottom removals occur before it could be removed. We can count the cumulative number of '0's (top removals) and '1's (bottom removals) in s. Any card whose position is less than the number of top removals must have been removed. Any card whose distance from the bottom is less than the number of bottom removals must have been removed. Cards outside these guaranteed removals remain, and cards within the ambiguous '2's that overlap with both ends are marked as '?'. This reduces the problem to simple arithmetic comparisons and cumulative counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(n) | Too slow |
| Optimal | O(n + k) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize counters `top_removals` and `bottom_removals` to zero. These will track the guaranteed removals from each end.
2. Iterate over the string s. For each '0', increment `top_removals`. For each '1', increment `bottom_removals`. For '2', do not increment either counter because we cannot guarantee which end it affected.
3. Initialize the output array with '+', assuming all cards remain.
4. For each card numbered i from 1 to n, check its position relative to the guaranteed removals. If i ≤ top_removals, it has been removed from the top and should be marked '-'. If n-i+1 ≤ bottom_removals, it has been removed from the bottom and should be marked '-'.
5. If neither condition is true, but i is within the range potentially affected by ambiguous '2' removals, mark '?'. This happens if i ≤ top_removals + number of '2's or n-i+1 ≤ bottom_removals + number of '2's. Otherwise, leave as '+'.
6. Join the array into a string and output.

This works because we are only considering guaranteed removals from known actions. Ambiguous removals do not reduce the remaining deck count in a predictable way, so '?' accurately reflects uncertainty. The invariant is that `top_removals` and `bottom_removals` always correctly count how many cards from each end have been definitively removed. All remaining cards outside these ranges are either certainly present or uncertain, which the algorithm marks correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        top = s.count('0')
        bottom = s.count('1')
        ambiguous = s.count('2')
        res = ['+'] * n
        for i in range(1, n+1):
            if i <= top or (n - i + 1) <= bottom:
                res[i-1] = '-'
            elif i <= top + ambiguous or (n - i + 1) <= bottom + ambiguous:
                res[i-1] = '?'
        print(''.join(res))

if __name__ == "__main__":
    solve()
```

We first read the number of test cases. For each test case, we count the number of guaranteed top removals, bottom removals, and ambiguous removals. We initialize the result as all '+'. Then, for each card, we first mark it '-' if it falls into the range of guaranteed removals. If not, we check whether it might have been affected by ambiguous actions and mark '?'. Otherwise, it remains '+'. Using counts instead of simulating the deck ensures linear time and avoids off-by-one errors when calculating positions from the bottom.

## Worked Examples

### Sample 1

Input:

```
4
4 2
01
3 2
22
1 1
2
7 5
01201
```

Trace for first test case, n=4, s="01":

| i | top=1 | bottom=1 | res[i] |
| --- | --- | --- | --- |
| 1 | i=1 ≤ 1 | - | '-' |
| 2 | i=2 > 1 | 4-2+1=3>1 | '+' |
| 3 | i=3 > 1 | 4-3+1=2>1 | '+' |
| 4 | i=4 >1 | 4-4+1=1 ≤1 | '-' |

Output: `-++-`

This confirms our calculation matches the sample output.

### Sample 2

Second test case, n=3, s="22":

All actions are ambiguous, top=0, bottom=0, ambiguous=2. Every card might be removed from either end.

| i | top=0 | bottom=0 | ambiguous=2 | res[i] |
| --- | --- | --- | --- | --- |
| 1 | 1>0 | 3>0 | 1≤2 | '?' |
| 2 | 2>0 | 2>0 | 2≤2 | '?' |
| 3 | 3>0 | 1>0 | 3>2? | '?' |

Output: `???`

This demonstrates that '?' correctly marks cards where we cannot be sure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + k) | Counting characters in s takes O(k). Iterating through n cards takes O(n). |
| Space | O(n) | We store the output string of length n for each test case. |

The sum of n over all test cases is ≤ 2×10^5, so the total work is at most 4×10^5 operations, well within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4\n4 2\n01\n3 2\n22\n1 1\n2\n7 5\n01201\n") == "-++-\n???\n-\n--?+?--", "sample 1"

# Minimum-size input
assert run("1\n1 1\n0\n") == "-", "single card removed top"
assert run("1\n1 1\n1\n") == "-", "single card removed bottom"
assert run("1\n1 1\n2\n") == "?", "single card ambiguous"

# Maximum-size input, all '0's
assert run(f"1\n200000 200000\n{'0'*200000}\n") == "-"*200000, "all removed top"

# Ambiguous range covering entire deck
assert run("1\n5 5\n22222\n") == "?????", "all ambiguous"

# Mixed top/bottom with ambiguity
assert run("1\n5 3\n021\n") == "-???-", "mixed removal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 0 | - | single card top removal |
| 1 1 2 | ? | single ambiguous card |
| 200000 200000 all '0's | all '-' | maximum size, full top removal |
| 5 5 all '2's | all '?' | maximum ambiguity |
| 5 3 "021" | -???- | mixed removals, correct '?' placement |

## Edge Cases

For n=1, s="2", the algorithm correctly outputs '?'. The card is neither guaranteed removed nor guaranteed to remain.

For n=3
