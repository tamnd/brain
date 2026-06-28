---
title: "CF 104846C - \u041f\u043e\u0438\u0441\u043a \u0441\u043e\u043a\u0440\u043e\u0432\u0438\u0449"
description: "We are given several chests, each containing a certain number of coins. Two friends want to split coins so that each chest ultimately contributes equally to both of them, but a chest can only be “cashed out” if its coin count is even."
date: "2026-06-28T11:27:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104846
codeforces_index: "C"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 2023-2024 (7-8 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104846
solve_time_s: 59
verified: true
draft: false
---

[CF 104846C - \u041f\u043e\u0438\u0441\u043a \u0441\u043e\u043a\u0440\u043e\u0432\u0438\u0449](https://codeforces.com/problemset/problem/104846/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several chests, each containing a certain number of coins. Two friends want to split coins so that each chest ultimately contributes equally to both of them, but a chest can only be “cashed out” if its coin count is even. If a chest has an odd number of coins, we are allowed to move all coins from one chest into another chest, effectively merging piles until we decide to process them.

Once a chest is processed, its coins are split equally between the two friends, so a chest with $x$ coins contributes $x/2$ coins to each person, but only if $x$ is even at the moment of processing.

The task is not to output a sequence of moves, but to compute the maximum number of coins each friend can end up with after optimally merging chests and processing them.

Even though the statement talks about individual chests, the key structural freedom is that we can repeatedly move entire piles, meaning we can effectively rearrange the coins arbitrarily into new groups before deciding which ones to split.

From a constraints perspective, we are clearly in a linear regime: only the sum and parity of values matter. Any solution that tries to simulate merging choices explicitly would become quadratic or worse and would fail immediately once $n$ grows large.

A common mistake is to think that individual chests have independent contributions. For example, one might try to greedily process even chests first and ignore odd ones. This breaks in cases like $1, 1, 8$, where merging the odd chests first increases usable even mass.

Another pitfall is assuming that odd chests are inherently useless. For instance, in input $3, 1, 1$, the two odd chests can be merged into $2$, making them fully usable. Treating each chest independently loses this effect.

## Approaches

A brute-force interpretation would try all ways of merging chests into groups and then decide which groups become even and get processed. Each grouping changes the sums, and for each grouping we would compute how many coins can be distributed. The number of partitions of $n$ items grows super-exponentially, and even restricting ourselves to pairwise merges leads to an exponential search space. This approach quickly becomes infeasible once $n$ exceeds a small number.

The key observation is that merging removes structure entirely: we are never restricted by which original chest a coin came from. Any sequence of merges allows us to rearrange coins into arbitrary piles, meaning the only real invariant of the system is the total sum of all coins and whether we can eliminate a single leftover coin when the sum is odd.

Once we view the process this way, the problem stops being about chests and becomes about how many coins can be paired. Every operation effectively allows us to rearrange coins so that all but possibly one coin participate in a valid even split. That reduces the problem to maximizing how many full pairs of coins we can form globally.

This leads directly to the conclusion that each friend receives exactly half of all coins except possibly one leftover coin that cannot be paired.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force grouping and merging | Exponential | Exponential | Too slow |
| Sum + parity reduction | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the input once and compute the total number of coins across all chests.

1. Compute the sum of all $a_i$. This represents the total amount of material available for splitting. No merging operation changes this sum, so it is the only global quantity that matters.
2. Observe the parity of the sum. If the total is even, every coin can be paired with another coin in some arrangement, so all coins contribute fully to the split.
3. If the total is odd, exactly one coin will inevitably remain unpaired regardless of how we merge chests, because merging preserves total parity. That single coin cannot be part of any valid even split and effectively becomes unusable.
4. The final answer is half of the usable coins, meaning $\lfloor \text{sum} / 2 \rfloor$.

### Why it works

Merging allows arbitrary redistribution of coins, so the identity of original chests is irrelevant. The only constraint that survives all operations is parity: splitting requires even totals, and every valid split consumes coins in pairs. Since pairing is global and unrestricted, the best possible outcome is to pair as many coins as possible across the entire multiset. At most one coin can remain unpaired, so the maximum usable mass is the largest even number not exceeding the total sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

total = sum(a)
print(total // 2)
```

The implementation mirrors the reduction directly. The sum is accumulated once, and integer division by two automatically handles both even and odd cases without needing explicit parity checks.

A subtle point is that no simulation of merging is needed. Even though the statement emphasizes moving entire chests, this operation only serves to justify that arbitrary regrouping is possible, not to require explicit execution.

## Worked Examples

Consider an input like:

$1, 8, 2$

We track the total sum and resulting answer.

| Step | Array State | Total Sum | Interpretation |
| --- | --- | --- | --- |
| 1 | [1, 8, 2] | 11 | All coins collected |
| 2 | merged conceptually | 11 | Redistribution allowed |
| 3 | final | 5 | floor(11/2) |

This shows that even though the first chest is odd and unusable alone, it still contributes through merging.

Now consider:

$3, 1, 1$

| Step | Array State | Total Sum | Interpretation |
| --- | --- | --- | --- |
| 1 | [3, 1, 1] | 5 | Two odd values present |
| 2 | merge odds | 5 | can form even + leftover coin |
| 3 | final | 2 | floor(5/2) |

This demonstrates that odd elements are not wasted if they can be paired through merging, but one coin may still remain unmatched globally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass to compute sum |
| Space | O(1) | only accumulator used |

The algorithm is optimal for the input scale because any solution must at least read all values, which already costs linear time. Memory usage is constant since no structure beyond the running sum is needed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    return str(sum(a) // 2)

# provided samples (reconstructed format where needed)
assert run("3\n1 8 2\n") == "5"

# single chest
assert run("1\n10\n") == "5"

# all odd
assert run("3\n1 1 1\n") == "1"

# all even
assert run("4\n2 4 6 8\n") == "10"

# mixed case
assert run("5\n3 1 4 1 5\n") == str((3+1+4+1+5)//2)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 8 2 | 5 | basic mixed parity |
| 1 10 | 5 | single element |
| 3 1 1 1 | 1 | all odd handling |
| 4 2 4 6 8 | 10 | all even aggregation |
| 5 3 1 4 1 5 | 7 | general correctness |

## Edge Cases

A single-chest input like $10$ tests whether the solution incorrectly tries to require merging to another chest. Here the algorithm simply computes $10 // 2 = 5$, which matches the only possible split.

An all-odd configuration like $1, 1, 1$ tests whether leftover parity is handled globally rather than per chest. The sum is 3, so the answer becomes 1, reflecting that one coin cannot be paired after optimal merging.

A large all-even case such as $2, 4, 6, 8$ confirms that no artificial constraints are introduced by the logic. The sum is 20, and full pairing is always achievable, giving 10 to each friend.
