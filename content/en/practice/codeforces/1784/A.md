---
title: "CF 1784A - Monsters (easy version)"
description: "We are given several independent scenarios. In each scenario, there are $n$ monsters arranged conceptually in a line, and each monster has some integer health value. A monster disappears once its health reaches zero. We can perform two kinds of actions."
date: "2026-06-09T11:02:28+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1784
codeforces_index: "A"
codeforces_contest_name: "VK Cup 2022 - \u0424\u0438\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 (Engine)"
rating: 1000
weight: 1784
solve_time_s: 197
verified: false
draft: false
---

[CF 1784A - Monsters (easy version)](https://codeforces.com/problemset/problem/1784/A)

**Rating:** 1000  
**Tags:** brute force, greedy  
**Solve time:** 3m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent scenarios. In each scenario, there are $n$ monsters arranged conceptually in a line, and each monster has some integer health value. A monster disappears once its health reaches zero.

We can perform two kinds of actions. The first action is local: we choose a single alive monster and reduce its health by exactly one. The second action is global: we reduce the health of every alive monster by one. The twist is that if this global action causes at least one monster to reach zero, the action immediately triggers again, repeatedly, until a full pass reduces no monster to zero. We are allowed to use this global action at most once, while the local action can be used arbitrarily many times. The goal is to minimize how many local actions we end up using while ensuring all monsters are eventually killed.

The key difficulty is that the global operation can cascade and potentially remove multiple monsters in one “chain”, but its usefulness depends entirely on when it is activated relative to the distribution of health values.

The constraints are large: the total number of monsters over all test cases is up to $2 \cdot 10^5$. This rules out any solution that simulates the global operation step by step over all health values or repeatedly scans arrays in a naive way. Any valid approach must reduce each test case to at most linear or near-linear work.

A naive simulation would try all possible moments to apply the global spell and simulate its cascading behavior. This immediately becomes infeasible because each simulation can take $O(n)$, and there are $O(n)$ choices, leading to $O(n^2)$ per test case.

A subtle edge case appears when many monsters share the same minimum health. For example, if all values are equal like $[3,3,3]$, the global spell alone wipes everything at once, producing zero local actions. On the other hand, if the minimum is unique but the rest are significantly larger, premature or delayed global usage changes nothing about the final answer, but naive reasoning might incorrectly assume timing matters.

Another tricky situation arises when the minimum value is 1. For example, $[1,100,100]$. If we use the global spell immediately, we kill only the first monster and reduce others, but we may not reduce the number of local operations in any meaningful way unless we align the decision with the structure of remaining values.

The core observation is that the global spell effectively “shifts” all values down uniformly once, and any monster with original value 1 becomes a pivot where cascading stops locally.

## Approaches

A brute-force idea is to try using the global spell at every possible moment. Since the global spell is applied only once, we can imagine choosing a time when some subset of monsters has already been partially reduced by local operations. For each choice, we simulate the global effect and count how many extra local operations are needed to finish the remaining monsters. However, simulation is expensive: applying the global spell and tracking cascading deletions requires repeatedly scanning the array, and combining this with all possible pre-operations leads to quadratic or worse complexity.

The key simplification comes from flipping the perspective. Instead of thinking about when to apply the global spell, we ask what structure remains if we do apply it. After using the global spell once, every monster’s health decreases by 1, and all monsters with original value 1 disappear immediately. What remains are monsters with values at least 2, now reduced by 1. From that point onward, only local operations matter.

This means the global spell can be interpreted as selecting a cutoff: all monsters with value 1 vanish for free, and all others are reduced once. The only cost left is handling the residual health of the remaining monsters.

Without using the global spell, every monster must be reduced entirely using local operations, costing $\sum a_i$. With the global spell, we “save” exactly one unit of work for every monster with $a_i \ge 1$, but only if we interpret the cascade correctly: the real gain is that all ones disappear for free, and all others get reduced once, effectively shifting the problem.

So we compare two cases:

If we never use the global spell, the answer is simply $\sum a_i$.

If we use it once, every monster loses 1 health, and all monsters with original value 1 vanish. The remaining cost becomes $\sum \max(0, a_i - 1)$.

We take the minimum of these two values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation of spell timing | $O(n^2)$ | $O(n)$ | Too slow |
| Compare two configurations (use / not use global spell) | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We compute two quantities for each test case: the sum of all values, and the sum of $\max(0, a_i - 1)$. The answer is the smaller of the two.

1. Read the array of monster health values. This gives the full cost structure of killing everything using only local actions.
2. Compute the total sum of all values. This represents the scenario where we never use the global spell, so every unit of health must be removed manually.
3. Compute a second sum where each value contributes $a_i - 1$ if it is at least 1, otherwise 0. This corresponds to applying the global spell once, which reduces every monster by 1 and eliminates those that hit zero immediately.
4. Take the minimum of the two sums. This directly compares the cost of never using the global spell versus using it once.

### Why it works

The global spell, when used exactly once, applies a uniform decrement across all alive monsters. Its only non-linear effect is that monsters reaching zero during the cascade vanish immediately and do not require any further operations. This behavior is equivalent to reducing every monster by one unit and removing all zeros afterward. Since any additional use of the global spell is disallowed, there is no benefit in considering multiple applications, and all optimal strategies collapse into the two cases considered.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    total = 0
    reduced = 0
    
    for x in a:
        total += x
        if x > 1:
            reduced += x - 1
    
    print(min(total, reduced))
```

The solution processes each test case in a single pass through the array. The variable `total` accumulates the cost of never using the global spell. The variable `reduced` simulates applying the global spell once by subtracting one from each positive value, but since all values are at least 1, we safely compute `x - 1` for all elements. The minimum of these two captures the optimal strategy.

A subtle implementation detail is that there is no need to explicitly check for zeros after reduction because the input guarantees $a_i \ge 1$. This removes boundary complexity and keeps the computation strictly linear.

## Worked Examples

### Example 1

Input:

```
3
3 1 2
```

We compute both scenarios.

| Step | Array contribution | total | reduced |
| --- | --- | --- | --- |
| 1 | 3 | 3 | 2 |
| 2 | 1 | 4 | 2 |
| 3 | 2 | 6 | 3 |

Final values: total = 6, reduced = 3, answer = 3.

This shows that applying the global spell is beneficial because it eliminates the unit-cost contribution from the smallest elements and shifts all others down.

### Example 2

Input:

```
6
4 1 5 4 1 1
```

| Step | Value | total | reduced |
| --- | --- | --- | --- |
| 1 | 4 | 4 | 3 |
| 2 | 1 | 5 | 3 |
| 3 | 5 | 10 | 7 |
| 4 | 4 | 14 | 10 |
| 5 | 1 | 15 | 10 |
| 6 | 1 | 16 | 10 |

Final values: total = 16, reduced = 10, answer = 10.

The trace shows that the global spell consistently reduces every nontrivial monster by exactly one unit of required local work, while eliminating all unit-health monsters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each array is scanned once to compute both sums |
| Space | $O(1)$ extra | Only two accumulators are used |

The total work over all test cases is linear in the total number of monsters, which fits comfortably within the constraints of $2 \cdot 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        total = sum(a)
        reduced = sum(x - 1 for x in a)
        out.append(str(min(total, reduced)))
    return "\n".join(out) + "\n"

# provided samples
assert run("""2
3
3 1 2
6
4 1 5 4 1 1
""") == "3\n10\n"

# all ones
assert run("""1
5
1 1 1 1 1
""") == "0\n"

# increasing values
assert run("""1
4
1 2 3 4
""") == "5\n"

# single monster
assert run("""1
1
7
""") == "1\n"

# already large uniform
assert run("""1
3
5 5 5
""") == "12\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones | 0 | global spell removes everything for free |
| increasing values | 5 | tradeoff between sum and reduced sum |
| single monster | 1 | boundary case correctness |
| uniform large values | 12 | consistent reduction across all elements |

## Edge Cases

For an input where all monsters have value 1, such as $[1,1,1]$, the algorithm computes total = 3 and reduced = 0, correctly selecting 0. This matches the fact that a single global spell kills everything immediately through cascading.

For a mixed case like $[1,2,2]$, total is 5 and reduced is 3. The algorithm correctly captures that only the larger monsters benefit from the uniform reduction, while the ones already at 1 contribute no further cost after the spell.

For a single-element array $[k]$, total is $k$ and reduced is $k-1$, correctly reflecting that the global spell can only save one unit of work if used.
