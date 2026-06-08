---
title: "CF 1879A - Rigged!"
description: "We have a weightlifting competition with n athletes. Athlete i has strength si and endurance ei. A barbell weight w is chosen. Any athlete whose strength is less than w cannot lift the barbell at all. Any athlete whose strength is at least w lifts it exactly ei times."
date: "2026-06-08T22:48:36+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1879
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 155 (Rated for Div. 2)"
rating: 800
weight: 1879
solve_time_s: 330
verified: true
draft: false
---

[CF 1879A - Rigged!](https://codeforces.com/problemset/problem/1879/A)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 5m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a weightlifting competition with `n` athletes. Athlete `i` has strength `s_i` and endurance `e_i`.

A barbell weight `w` is chosen. Any athlete whose strength is less than `w` cannot lift the barbell at all. Any athlete whose strength is at least `w` lifts it exactly `e_i` times. The winner is the unique athlete with the highest number of lifts. If several athletes tie for the highest number, nobody wins.

Polycarp is athlete `1`. We must determine whether there exists some weight `w` that makes Polycarp the unique winner. If such a weight exists, we may output any valid value of `w`. Otherwise we output `-1`.

The constraints are very small. There are at most `100` athletes per test case and at most `100` test cases. Even an `O(n²)` solution is trivial here. The large strength values do not matter because we never need to iterate through all possible weights. We only need to reason about which athletes remain eligible for a given choice of `w`.

A common mistake is to focus on finding an explicit winning weight immediately. Consider:

```
Polycarp: (7, 4)
Other:    (9, 3)
```

Choosing `w = 5` allows both athletes to compete, but Polycarp wins because `4 > 3`.

Another easy mistake is forgetting ties. Consider:

```
Polycarp: (1337, 3)
Other:    (1337, 3)
```

Any weight that allows Polycarp also allows the other athlete. Their lift counts are equal, so there is never a unique winner. The answer is `-1`.

A third subtle case occurs when another athlete is stronger and has at least as much endurance:

```
Polycarp: (4, 6)
Other:    (100, 100)
```

Any weight that lets Polycarp participate also lets the other athlete participate, because the other athlete is stronger. Since the other athlete lifts more times, Polycarp can never win.

## Approaches

A brute force viewpoint is to try every relevant barbell weight and simulate the competition. Since strengths can be as large as `10^9`, iterating over all possible weights is impossible. We could reduce the search to the distinct strength values that appear in the input, because the set of eligible athletes only changes when we cross a strength threshold. That would already be fast enough for these constraints.

There is an even simpler observation.

Suppose another athlete has both strength at least Polycarp's strength and endurance at least Polycarp's endurance. Then whenever Polycarp can lift the barbell, that athlete can also lift it. Since the athlete's endurance is not smaller, Polycarp can never be the unique winner.

Conversely, if no athlete satisfies both conditions simultaneously, choosing

```
w = s₁
```

makes Polycarp eligible. Any athlete with strength below `s₁` is eliminated immediately. Any athlete with strength at least `s₁` must have endurance strictly less than `e₁`, otherwise they would satisfy both conditions. Hence Polycarp has strictly larger endurance than every remaining competitor and becomes the unique winner.

This turns the entire problem into checking whether there exists an athlete `i > 1` such that

```
s_i ≥ s₁ and e_i ≥ e₁.
```

If such an athlete exists, the answer is `-1`. Otherwise `w = s₁` works.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over relevant weights | O(n²) | O(1) | Accepted |
| Dominance observation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read Polycarp's strength `s₁` and endurance `e₁`.
2. For every other athlete, check whether both conditions hold:

```
s_i ≥ s₁
e_i ≥ e₁
```
3. If such an athlete exists, print `-1`.

This athlete is at least as strong and at least as enduring as Polycarp. Whenever Polycarp can participate, this athlete can participate too, preventing a unique Polycarp victory.
4. If no such athlete exists, print `s₁`.

Choosing `w = s₁` guarantees that Polycarp participates. Every other participating athlete must have endurance strictly less than `e₁`, so Polycarp wins uniquely.

### Why it works

An athlete can only threaten Polycarp if they are still eligible whenever Polycarp is eligible. That requires strength at least `s₁`.

Among those athletes, the only ones capable of preventing Polycarp from being the unique winner are those whose endurance is at least `e₁`.

Thus the existence of an athlete with

```
s_i ≥ s₁ and e_i ≥ e₁
```

is exactly the condition that makes victory impossible.

If no such athlete exists, selecting `w = s₁` eliminates all weaker athletes and leaves only athletes with strictly smaller endurance than Polycarp. Therefore Polycarp becomes the unique winner.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())

        s1, e1 = map(int, input().split())
        possible = True

        for _ in range(n - 1):
            s, e = map(int, input().split())

            if s >= s1 and e >= e1:
                possible = False

        print(s1 if possible else -1)

solve()
```

The implementation follows the proof directly.

We store Polycarp's parameters and scan through the remaining athletes once. If we ever find an athlete whose strength and endurance are both at least Polycarp's values, we mark the answer as impossible.

There is no need to store all athletes because each competitor is examined independently. The solution uses constant extra memory.

The comparison must use `>=` rather than `>`. An athlete with exactly the same endurance still causes a tie and prevents a unique winner.

## Worked Examples

### Example 1

Input:

```
4
7 4
9 3
4 6
2 2
```

| Athlete | Strength ≥ 7? | Endurance ≥ 4? | Blocks Polycarp? |
| --- | --- | --- | --- |
| (9, 3) | Yes | No | No |
| (4, 6) | No | Yes | No |
| (2, 2) | No | No | No |

No athlete satisfies both conditions.

Output:

```
7
```

A valid sample answer is `5`, but any valid weight is accepted. Choosing `w = 7` also makes Polycarp the unique winner.

### Example 2

Input:

```
2
4 6
100 100
```

| Athlete | Strength ≥ 4? | Endurance ≥ 6? | Blocks Polycarp? |
| --- | --- | --- | --- |
| (100, 100) | Yes | Yes | Yes |

A blocking athlete exists.

Output:

```
-1
```

This example demonstrates the core impossibility condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass through the athletes |
| Space | O(1) | Only a few variables are stored |

Since `n ≤ 100`, the solution is vastly below the time limit. Even with the maximum number of test cases, the total amount of work is tiny.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = []
    t = int(input())

    for _ in range(t):
        n = int(input())

        s1, e1 = map(int, input().split())
        ok = True

        for _ in range(n - 1):
            s, e = map(int, input().split())
            if s >= s1 and e >= e1:
                ok = False

        out.append(str(s1 if ok else -1))

    return "\n".join(out)

# provided sample
assert run(
"""3
4
7 4
9 3
4 6
2 2
2
4 6
100 100
2
1337 3
1337 3
"""
) == "7\n-1\n-1"

# equal athlete causes tie
assert run(
"""1
2
10 5
10 5
"""
) == "-1"

# stronger but lower endurance does not block
assert run(
"""1
2
10 5
100 4
"""
) == "10"

# weaker but higher endurance does not block
assert run(
"""1
2
10 5
9 100
"""
) == "10"

# minimum n
assert run(
"""1
2
1 1
2 2
"""
) == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Equal athlete | -1 | Tie prevents a unique winner |
| Stronger, lower endurance | Polycarp strength | Both conditions are required |
| Weaker, higher endurance | Polycarp strength | Strength condition matters |
| Minimum size case | -1 | Smallest valid input |

## Edge Cases

Consider:

```
1
2
10 5
10 5
```

The second athlete has identical parameters. The algorithm detects

```
10 ≥ 10
5 ≥ 5
```

and outputs `-1`. Any weight that allows Polycarp also allows the other athlete, producing a tie.

Consider:

```
1
2
10 5
100 4
```

The second athlete is stronger but has lower endurance. The algorithm sees that the endurance condition fails and outputs `10`. Choosing `w = 10` allows both athletes to compete, but Polycarp lifts the barbell five times while the other athlete lifts it four times.

Consider:

```
1
2
10 5
9 100
```

The second athlete has enormous endurance but insufficient strength. Choosing `w = 10` eliminates that athlete completely. The algorithm correctly outputs `10`.

Consider:

```
1
2
4 6
100 100
```

The second athlete dominates Polycarp in both strength and endurance. No matter which valid weight is chosen, if Polycarp can lift the barbell then the second athlete can too, and the second athlete lifts more times. The algorithm detects this domination and outputs `-1`.
