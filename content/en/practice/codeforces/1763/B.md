---
title: "CF 1763B - Incinerate"
description: "We are fighting a set of monsters. Every monster has a health value and a power value. Genos repeatedly performs attacks. If the current attack strength is k, every monster that is still alive loses k health simultaneously."
date: "2026-06-09T13:44:28+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1763
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 840 (Div. 2) and Enigma 2022 - Cybros LNMIIT"
rating: 1200
weight: 1763
solve_time_s: 671
verified: false
draft: false
---

[CF 1763B - Incinerate](https://codeforces.com/problemset/problem/1763/B)

**Rating:** 1200  
**Tags:** binary search, brute force, data structures, implementation, math, sortings  
**Solve time:** 11m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are fighting a set of monsters. Every monster has a health value and a power value.

Genos repeatedly performs attacks. If the current attack strength is `k`, every monster that is still alive loses `k` health simultaneously. After that attack, we look at the monsters that remain alive. Among them, find the minimum power value. That minimum power is subtracted from `k`, reducing the strength of all future attacks.

The process continues until either every monster dies, which means the answer is `"YES"`, or the attack strength becomes non-positive while some monster is still alive, which means the answer is `"NO"`.

The input gives multiple test cases. For each test case we know the initial attack strength `k`, the health of every monster, and the power of every monster. We must determine whether all monsters can eventually be eliminated.

The constraints are the first thing that should guide the solution. A single health or power can be as large as `10^9`, and `k` can also be `10^9`. Simulating attacks one by one is impossible because there could be billions of attacks before all monsters die. The total number of monsters across all test cases is only `2·10^5`, which strongly suggests that the solution should spend roughly `O(n log n)` or `O(n)` work per test case.

A subtle edge case appears when several monsters die at the same attack. The weakest alive monster after the attack may be completely different from the weakest monster before the attack.

Consider:

```
n = 2, k = 5
h = [5, 100]
p = [1, 100]
```

After the first attack, the first monster dies immediately. The next reduction must use power `100`, not power `1`, because the weakest surviving monster now has power `100`.

Another easy mistake is to simulate health values directly. Health values can be as large as `10^9`, so repeatedly subtracting damage from every monster would be far too slow.

A third trap is assuming monsters should be processed by health. The power values determine how quickly future attacks weaken, so sorting only by health loses critical information.

For example:

```
h = [10, 20]
p = [100, 1]
```

The low-power monster is strategically important because killing it late keeps attack strength high for longer.

## Approaches

A brute-force simulation would repeatedly perform attacks. During each attack we would subtract the current damage from every alive monster, determine which monsters remain alive, find the minimum power among them, reduce `k`, and continue.

This is correct because it directly follows the rules. Unfortunately, the number of attacks is not bounded by `n`. Attack strengths and health values can reach `10^9`, so the process may require an enormous number of iterations. Even if each attack took only `O(n)`, the total work would be completely infeasible.

The key observation is that only the moments when monsters die actually matter.

Let `damage` denote the total damage dealt so far to every monster. A monster dies once `damage ≥ h_i`.

Suppose we know the current accumulated damage `damage`. Then every monster with `h_i ≤ damage` is already dead. Among the remaining monsters, the smallest power determines how much attack strength will decrease after the next attack.

This suggests sorting monsters by health. Once sorted, we can efficiently determine which monsters have already died as total accumulated damage grows.

The second observation is that we only need to know the minimum power among monsters whose health is still greater than the current accumulated damage. This can be maintained with a suffix minimum array.

After sorting by health:

```
(h1,p1), (h2,p2), ...
```

define

```
suf[i] = min power among monsters i..n-1
```

If all monsters with index less than `ptr` are dead, then the weakest alive monster has power `suf[ptr]`.

Now the process becomes very compact:

We maintain total accumulated damage `damage`.

Each iteration adds current attack strength `k` to `damage`.

We advance a pointer past every monster whose health is now at most `damage`.

If all monsters are dead, answer `"YES"`.

Otherwise, the weakest surviving power is `suf[ptr]`, so we decrease `k` by that amount.

The number of iterations is at most `n`, because every iteration either kills at least one new monster or makes `k` non-positive.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Unbounded, potentially billions of attacks | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Pair each monster's health and power into `(h_i, p_i)`.
2. Sort the monsters by health.
3. Build a suffix minimum array of powers. For every position `i`, `suf[i]` stores the minimum power among monsters from `i` to the end.
4. Initialize:

- `damage = 0`
- `ptr = 0`
5. While `k > 0`:

1. Add the current attack strength to total damage:

`damage += k`.
2. Move `ptr` forward while `health[ptr] ≤ damage`.

These monsters are already dead.
3. If `ptr == n`, every monster has died. Output `"YES"`.
4. Otherwise, the weakest surviving monster has power `suf[ptr]`. Reduce attack strength:

`k -= suf[ptr]`.
6. If the loop ends because `k ≤ 0` and some monsters are still alive, output `"NO"`.

### Why it works

The accumulated damage after several attacks is exactly the total amount subtracted from every monster's health. A monster is alive precisely when its health exceeds this accumulated damage.

At any moment, future attack strength reduction depends only on the minimum power among alive monsters. After sorting by health, the alive monsters always form a suffix of the array because every monster with smaller health dies no later than a monster with larger health.

The suffix minimum array gives the minimum power among all alive monsters in constant time. Every iteration exactly reproduces the same state transition as the original process, but without tracking individual health values. Since the simulation remains mathematically identical, the algorithm produces the same result as the original game.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    answers = []

    for _ in range(t):
        n, k = map(int, input().split())
        h = list(map(int, input().split()))
        p = list(map(int, input().split()))

        monsters = sorted(zip(h, p))

        suf = [0] * n
        suf[-1] = monsters[-1][1]

        for i in range(n - 2, -1, -1):
            suf[i] = min(suf[i + 1], monsters[i][1])

        damage = 0
        ptr = 0
        cur_k = k

        while cur_k > 0:
            damage += cur_k

            while ptr < n and monsters[ptr][0] <= damage:
                ptr += 1

            if ptr == n:
                answers.append("YES")
                break

            cur_k -= suf[ptr]
        else:
            answers.append("NO")

    sys.stdout.write("\n".join(answers))

solve()
```

The sorting step creates the order in which monsters can disappear. Once total accumulated damage reaches a monster's health, that monster is dead forever, so the alive monsters always occupy a suffix of the sorted array.

The suffix minimum array is the critical optimization. Without it, every iteration would need to scan all surviving monsters to find the weakest power. With it, the weakest surviving power is available immediately.

The pointer `ptr` only moves forward. Each monster is skipped once, giving a total of `O(n)` pointer movement across the entire test case.

Using `damage` instead of updating every health individually avoids handling values as large as `10^9` repeatedly and keeps the simulation efficient.

## Worked Examples

### Example 1

Input:

```
n = 6, k = 7

h = [18,5,13,9,10,1]
p = [2,7,2,1,2,6]
```

After sorting:

| Index | Health | Power |
| --- | --- | --- |
| 0 | 1 | 6 |
| 1 | 5 | 7 |
| 2 | 9 | 1 |
| 3 | 10 | 2 |
| 4 | 13 | 2 |
| 5 | 18 | 2 |

Suffix minimum powers:

```
[1,1,1,2,2,2]
```

| Iteration | Current k | Damage After Attack | ptr | Weakest Alive Power |
| --- | --- | --- | --- | --- |
| 1 | 7 | 7 | 2 | 1 |
| 2 | 6 | 13 | 5 | 2 |
| 3 | 4 | 17 | 5 | 2 |
| 4 | 2 | 19 | 6 | dead |

All monsters are dead, so the answer is `"YES"`.

This example shows how multiple monsters can die simultaneously when accumulated damage jumps past several health thresholds.

### Example 2

Input:

```
n = 3, k = 4
h = [5,5,5]
p = [4,4,4]
```

Sorted order is unchanged.

| Iteration | Current k | Damage After Attack | ptr | Weakest Alive Power |
| --- | --- | --- | --- | --- |
| 1 | 4 | 4 | 0 | 4 |
| 2 | 0 | - | - | - |

The attack strength becomes zero before total damage reaches health 5, so monsters remain alive and the answer is `"NO"`.

This example demonstrates the failure condition where attack strength is exhausted first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the running time |
| Space | O(n) | Sorted array and suffix minimum array |

The total number of monsters across all test cases is at most `2·10^5`. An `O(n log n)` solution comfortably fits within the time limit, and the linear auxiliary storage easily fits within the memory limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, k = map(int, input().split())
        h = list(map(int, input().split()))
        p = list(map(int, input().split()))

        monsters = sorted(zip(h, p))

        suf = [0] * n
        suf[-1] = monsters[-1][1]

        for i in range(n - 2, -1, -1):
            suf[i] = min(suf[i + 1], monsters[i][1])

        damage = 0
        ptr = 0
        cur_k = k

        while cur_k > 0:
            damage += cur_k

            while ptr < n and monsters[ptr][0] <= damage:
                ptr += 1

            if ptr == n:
                out.append("YES")
                break

            cur_k -= suf[ptr]
        else:
            out.append("NO")

    return "\n".join(out)

# provided samples
assert run(
"""3
6 7
18 5 13 9 10 1
2 7 2 1 2 6
3 4
5 5 5
4 4 4
3 2
2 1 3
1 1 1
"""
) == "YES\nNO\nYES"

# minimum size
assert run(
"""1
1 1
1
1
"""
) == "YES"

# immediate failure
assert run(
"""1
1 1
2
5
"""
) == "NO"

# all monsters die in first attack
assert run(
"""1
4 100
1 2 3 4
10 20 30 40
"""
) == "YES"

# power changes after weakest dies
assert run(
"""1
2 5
5 100
1 100
"""
) == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single monster with health 1 | YES | Minimum-size success case |
| Single monster with health 2 and k=1 | NO | Attack strength exhausted |
| Very large first attack | YES | Multiple monsters die at once |
| Powers `[1,100]` | NO | Correct weakest-alive update after deaths |

## Edge Cases

Consider a case where all monsters have identical health:

```
1
3 5
5 5 5
1 2 3
```

After the first attack, accumulated damage becomes 5. Every monster dies simultaneously, the pointer moves directly to `n`, and the algorithm outputs `"YES"`. A solution that updates monsters one at a time could accidentally apply an extra power reduction after everyone is already dead.

Consider a case where the attack strength reaches exactly zero:

```
1
1 4
5
4
```

After the first attack, accumulated damage is 4 and the monster remains alive. The weakest alive power is 4, so attack strength becomes 0. The loop stops and the answer is `"NO"`. The algorithm correctly checks whether monsters are dead before applying the next attack.

Consider a case where several monsters die in one iteration:

```
1
4 10
3 4 5 100
1 1 1 1
```

Accumulated damage immediately becomes 10, killing the first three monsters. The pointer skips all three in one pass. The alive set remains a suffix of the sorted order, which is exactly the property that makes the suffix minimum technique valid.
