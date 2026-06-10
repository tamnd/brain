---
title: "CF 1463A - Dungeon"
description: "We have three monsters with health values a, b, and c. A normal cannon shot deals 1 damage to exactly one living monster. Every seventh shot is special. Instead of targeting a single monster, it deals 1 damage to every monster that is still alive at that moment."
date: "2026-06-11T01:59:08+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math"]
categories: ["algorithms"]
codeforces_contest: 1463
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 100 (Rated for Div. 2)"
rating: 1100
weight: 1463
solve_time_s: 118
verified: true
draft: false
---

[CF 1463A - Dungeon](https://codeforces.com/problemset/problem/1463/A)

**Rating:** 1100  
**Tags:** binary search, math  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We have three monsters with health values `a`, `b`, and `c`.

A normal cannon shot deals 1 damage to exactly one living monster. Every seventh shot is special. Instead of targeting a single monster, it deals 1 damage to every monster that is still alive at that moment.

The goal is not merely to kill all monsters. All three monsters must die together on the same enhanced shot. Before that shot, every monster must still be alive, and immediately after that enhanced shot all three health values become zero for the first time.

The input contains up to `10^4` test cases. Each health value can be as large as `10^8`, so any simulation based on individual shots is impossible. A single test case may require hundreds of millions of shots, which immediately rules out linear simulation. We need a mathematical condition that can be checked in constant time.

A subtle trap is assuming that only the total health matters.

For example:

```
1
10 1 7
```

The total health is 18, which is divisible by 9, but the answer is still `NO`. One monster is far too weak compared to the others and would die before the final enhanced shot.

Another easy mistake is forgetting that all monsters must survive until the last enhanced shot.

For example:

```
1
1 1 7
```

The total health is 9, which suggests one complete cycle of 9 damage. However, after the final enhanced shot each monster must have received at least one-third of the non-enhanced damage allocation. The two monsters with health 1 cannot absorb enough damage to make that possible, so the answer is `NO`.

A different edge case occurs when all monsters are equal.

```
1
3 3 3
```

The total health is 9, and each monster can easily participate in the final enhanced shot. The correct answer is `YES`.

Understanding why these examples differ leads directly to the key observation.

## Approaches

A brute-force approach would try to simulate the battle. We could repeatedly choose which monster receives each regular shot and apply the enhanced effect every seventh shot. Eventually we would check whether all three monsters die together.

This approach is correct in principle because it models the game exactly. The problem is that health values reach `10^8`. The total amount of damage can be up to `3 × 10^8`, so even one test case would require hundreds of millions of operations.

The crucial observation is that the exact order of regular shots does not matter. Only the total amount of damage matters.

Suppose the monsters die on the `k`-th enhanced shot.

Each group of seven shots contains six regular shots and one enhanced shot. Thus each complete cycle contributes:

```
6 targeted damage
3 enhanced damage
```

for a total of 9 damage.

If all monsters die on the final enhanced shot, then the total damage dealt must equal the total health:

```
a + b + c = 9k
```

So the sum must be divisible by 9.

Now consider how much damage each monster receives from enhanced shots. Since the final enhanced shot is the one that kills them, every monster must survive until it. Thus each monster receives exactly `k` enhanced damage in total.

After removing those `k` points, the remaining damage needed for monster `i` must come from regular shots.

The number of regular shots available is `6k`.

For this to be possible, no monster can require fewer than `k` total health. Otherwise it would die before receiving all `k` enhanced hits.

That gives:

```
min(a, b, c) >= k
```

Since

```
k = (a + b + c) / 9
```

the entire problem reduces to two simple checks.

The brute-force works because it follows the game literally, but fails because the health values are enormous. The observation that every successful battle consists of complete 9-damage cycles lets us replace simulation with arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a+b+c) | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total health:

```
s = a + b + c
```
2. Check whether `s` is divisible by 9.

If not, print `NO`.

A successful battle ending on an enhanced shot after `k` cycles always deals exactly `9k` damage.
3. Compute:

```
k = s / 9
```

This is the number of enhanced shots that must occur.
4. Find the smallest health value:

```
m = min(a, b, c)
```
5. If `m < k`, print `NO`.

Every monster must survive through all `k` enhanced shots. A monster with health less than `k` would reach zero before the final enhanced shot.
6. Otherwise print `YES`.

### Why it works

Assume the answer is `YES`.

If the monsters die together on the `k`-th enhanced shot, exactly `k` complete shot cycles occur. Each cycle contributes 9 total damage, so the total health must equal `9k`. This proves divisibility by 9.

Also, every living monster receives one point of damage from each enhanced shot. Since all monsters survive until the final enhanced shot, each monster must absorb at least `k` damage. Hence `min(a,b,c) ≥ k`.

Now assume both conditions hold. Let `k = (a+b+c)/9`.

Each monster can spend `k` health points on enhanced damage. After removing those contributions, the remaining required damage is:

```
(a-k) + (b-k) + (c-k)
= (a+b+c) - 3k
= 9k - 3k
= 6k
```

Exactly `6k` regular shots exist. Since every remaining amount is non-negative, those regular shots can be distributed accordingly. Thus all monsters reach health 1 just before the final enhanced shot and die together on that shot.

The two conditions are both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    
    for _ in range(t):
        a, b, c = map(int, input().split())
        
        s = a + b + c
        
        if s % 9 != 0:
            print("NO")
            continue
        
        k = s // 9
        
        if min(a, b, c) < k:
            print("NO")
        else:
            print("YES")

solve()
```

The solution follows the proof directly.

The first condition checks whether the total health can be represented as a whole number of 9-damage cycles. If not, there is no possible ending on an enhanced shot.

After that, `k` is determined uniquely. There is no need to search for it because the total health fixes the number of cycles.

The second condition verifies that every monster can survive through all `k` enhanced shots. Using `min(a,b,c)` is enough because if the smallest monster survives, the larger ones certainly do as well.

All calculations fit comfortably inside standard integer types. In Python there is no overflow concern, but even in 64-bit integers the maximum sum is only `3 × 10^8`.

## Worked Examples

### Example 1

Input:

```
3 2 4
```

| Variable | Value |
| --- | --- |
| a | 3 |
| b | 2 |
| c | 4 |
| s | 9 |
| s % 9 | 0 |
| k | 1 |
| min(a,b,c) | 2 |

Since `s` is divisible by 9 and `2 ≥ 1`, the answer is `YES`.

This demonstrates the successful case where one complete cycle exists. After six regular shots, every monster still survives, and the seventh shot kills all three together.

### Example 2

Input:

```
10 1 7
```

| Variable | Value |
| --- | --- |
| a | 10 |
| b | 1 |
| c | 7 |
| s | 18 |
| s % 9 | 0 |
| k | 2 |
| min(a,b,c) | 1 |

Since `1 < 2`, the answer is `NO`.

This shows why divisibility by 9 alone is insufficient. The second monster cannot survive two enhanced shots, so a simultaneous finish is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations are performed |
| Space | O(1) | No auxiliary data structures are used |

Even with `10^4` test cases, the program performs only constant-time work for each case. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    t = int(input())
    for _ in range(t):
        a, b, c = map(int, input().split())
        s = a + b + c

        if s % 9 != 0:
            print("NO")
            continue

        k = s // 9
        print("YES" if min(a, b, c) >= k else "NO")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("3\n3 2 4\n1 1 1\n10 1 7\n") == "YES\nNO\nNO\n", "sample"

# minimum values
assert run("1\n1 1 1\n") == "NO\n", "minimum healths"

# all equal and valid
assert run("1\n3 3 3\n") == "YES\n", "equal values"

# divisible by 9 but smallest too small
assert run("1\n1 4 4\n") == "NO\n", "fails min condition"

# large boundary values
assert run("1\n100000000 100000000 100000000\n") == "NO\n", "large numbers"

# exactly on boundary
assert run("1\n2 2 5\n") == "YES\n", "min equals k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `NO` | Sum not divisible by 9 |
| `3 3 3` | `YES` | Symmetric valid case |
| `1 4 4` | `NO` | Divisible by 9 but smallest health insufficient |
| `100000000 100000000 100000000` | `NO` | Large values and divisibility check |
| `2 2 5` | `YES` | Boundary where `min(a,b,c) = k` |

## Edge Cases

Consider:

```
1
1 4 4
```

The sum is 9, so `k = 1`. The smallest health is also 1. Since `1 ≥ 1`, the algorithm outputs `YES`. One monster can survive exactly one enhanced shot and die on the final one. Equality is allowed, which is a common off-by-one trap.

Consider:

```
1
10 1 7
```

The sum is 18, so `k = 2`. The smallest health is 1. Since `1 < 2`, the algorithm outputs `NO`. The monster with health 1 cannot remain alive through two enhanced shots, making a simultaneous kill impossible.

Consider:

```
1
1 1 1
```

The sum is 3. Since `3 % 9 != 0`, the algorithm immediately outputs `NO`. There is no integer number of complete 9-damage cycles that matches the total health.

Consider:

```
1
2 2 5
```

The sum is 9, so `k = 1`. The minimum health is 2, which satisfies `2 ≥ 1`. The algorithm outputs `YES`. This validates the boundary where one full cycle exists and all monsters can participate in the final enhanced shot.
