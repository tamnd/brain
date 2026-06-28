---
title: "CF 104802B - Snowy Bus"
description: "Each passenger has two attributes. Their mass contributes to the weight of the bus if they stay inside, while their pushing force contributes only if they get out and push. Suppose we choose some passengers as pushers."
date: "2026-06-28T16:44:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104802
codeforces_index: "B"
codeforces_contest_name: "TheForces Round #26 (Readall-Forces)"
rating: 0
weight: 104802
solve_time_s: 101
verified: false
draft: false
---

[CF 104802B - Snowy Bus](https://codeforces.com/problemset/problem/104802/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Problem Understanding

Each passenger has two attributes. Their mass contributes to the weight of the bus if they stay inside, while their pushing force contributes only if they get out and push.

Suppose we choose some passengers as pushers. Their total pushing force must be at least the weight that remains on the bus. The remaining weight consists of the empty bus plus the masses of every passenger who did not get out.

The task is to choose as few pushers as possible while satisfying this condition. If no choice of passengers can move the bus, the answer is `-1`.

The total number of passengers over all test cases is at most `2 × 10^5`. This immediately rules out trying every subset, since even `2^40` is already impossible, while `2^200000` is far beyond any practical computation. An `O(n^2)` algorithm is also too expensive because the worst case would require about `4 × 10^10` operations. An `O(n log n)` solution is easily fast enough for these limits.

Several edge cases deserve attention.

Consider a passenger whose force is much larger than everyone else's.

```
1
3 5
2 2 2
10 1 1
```

The correct answer is `1`. A strategy that simply removes the heaviest passengers first would incorrectly choose two people, even though the strongest passenger alone already succeeds.

Another important case is when moving the bus is impossible even if everyone gets out.

```
1
2 100
1 1
30 40
```

Even with every passenger pushing, the total force is only `70`, while the bus alone weighs `100`. The correct answer is `-1`.

A more subtle situation appears when two passengers have the same force but different masses.

```
1
2 5
100 1
10 10
```

Choosing the heavier passenger is always at least as good as choosing the lighter one because both contribute the same force, but removing the heavier passenger also removes more weight from the bus. A solution that ignores passenger mass while breaking ties can miss the optimal answer.

## Approaches

The most direct solution is to enumerate every subset of passengers. For each subset, compute the total pushing force and the remaining weight, then keep the smallest subset that satisfies the condition. This is correct because every possible choice is examined. Unfortunately, it requires `O(2^n · n)` time, which is completely infeasible.

The inequality describing a valid choice is

```
sum(force of chosen)
≥
w + sum(mass of unchosen)
```

Let `M` be the total mass of all passengers.

Since

```
sum(mass of unchosen)
=
M - sum(mass of chosen),
```

the condition becomes

```
sum(force) + sum(mass) ≥ w + M.
```

Now every chosen passenger contributes independently by adding

```
force + mass
```

toward a fixed target

```
w + M.
```

This transformation removes the interaction between chosen and unchosen passengers. Each passenger simply has a value

```
value = force + mass.
```

To minimize the number of selected passengers while reaching a target sum, the greedy strategy is obvious. Always take the largest available value first. If a solution using `k` passengers exists, then the `k` largest values achieve at least as much total contribution as any other `k` passengers.

After sorting these values in descending order, we keep taking passengers until the accumulated contribution reaches the target. If even all passengers together are insufficient, the answer is `-1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^n · n)` | `O(n)` | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read the masses and forces of all passengers.
2. Compute the total passenger mass `M`. The required contribution is `target = w + M`.
3. For every passenger, compute `value = mass + force`. This measures how much selecting that passenger helps. Their force increases the left side of the inequality, while removing their mass decreases the required weight by exactly the same amount.
4. Sort all values in descending order. Since we want the fewest passengers, every chosen passenger should provide as much contribution as possible.
5. Traverse the sorted values from largest to smallest, maintaining the accumulated contribution.
6. As soon as the accumulated contribution becomes at least `target`, output how many passengers have been taken. No smaller answer is possible because any other set with the same number of passengers has contribution no larger than the largest values already chosen.
7. If the entire list is processed without reaching the target, output `-1`.

### Why it works

The transformed inequality depends only on the sum of `mass + force` over the chosen passengers. Among all subsets containing exactly `k` passengers, the largest possible contribution is obtained by taking the `k` largest values. If these largest values fail to reach the target, then no other subset of size `k` can succeed. Conversely, once they do reach the target, a valid subset of size `k` exists. The first successful prefix of the sorted list is exactly the minimum number of required pushers.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, w = map(int, input().split())
        masses = list(map(int, input().split()))
        forces = list(map(int, input().split()))

        target = w + sum(masses)
        values = [m + f for m, f in zip(masses, forces)]
        values.sort(reverse=True)

        cur = 0
        ans = -1
        for i, v in enumerate(values, 1):
            cur += v
            if cur >= target:
                ans = i
                break

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part computes the target contribution, which is the empty bus weight plus the total passenger mass.

Each passenger is converted into a single value equal to their mass plus their force. This comes directly from the algebraic transformation of the original inequality.

Sorting these values in descending order lets the algorithm examine the best possible subset of every size. The running sum represents the maximum contribution achievable using the current number of passengers.

The first prefix whose sum reaches the target immediately gives the optimal answer. If the full prefix still falls short, then even selecting everyone cannot move the bus.

Python integers automatically handle the largest possible sums, so no overflow precautions are needed.

## Worked Examples

Consider the following test case.

```
1
3 4
1 1 1
6 3 3
```

The total passenger mass is `3`, so the target is `7`.

The passenger values are `[7, 4, 4]`.

| Step | Value Chosen | Running Sum | Target | Answer |
| --- | --- | --- | --- | --- |
| 1 | 7 | 7 | 7 | 1 |

The target is reached after selecting the first passenger, so only one pusher is needed.

Now consider an impossible example.

```
1
2 100
1 1
30 40
```

The total passenger mass is `2`, so the target is `102`.

The values are `[41, 31]`.

| Step | Value Chosen | Running Sum | Target | Answer |
| --- | --- | --- | --- | --- |
| 1 | 41 | 41 | 102 | Not reached |
| 2 | 31 | 72 | 102 | Not reached |

Even after selecting everyone, the contribution is only `72`, so the answer is `-1`.

The first trace demonstrates that a single strong passenger may be sufficient. The second confirms that the algorithm correctly detects when no feasible subset exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Sorting dominates the running time. |
| Space | `O(n)` | Stores the transformed values. |

Since the total number of passengers across all test cases is at most `2 × 10^5`, sorting each test case easily fits within the time limit, and the memory usage remains well below the allowed limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, w = map(int, input().split())
        m = list(map(int, input().split()))
        f = list(map(int, input().split()))
        target = w + sum(m)
        vals = sorted((a + b for a, b in zip(m, f)), reverse=True)
        s = 0
        ans = -1
        for i, v in enumerate(vals, 1):
            s += v
            if s >= target:
                ans = i
                break
        out.append(str(ans))
    print("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    res = sys.stdout.getvalue().strip()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return res

assert run("""4
3 4
1 1 1
6 6 6
3 4
1 1 1
3 3 3
1 1000
100
100
6 10
7 5 1 4 2 8
3 1 2 7 5 9
""") == "1\n2\n-1\n3", "sample"

assert run("""1
1 1
1
2
""") == "1", "minimum feasible"

assert run("""1
1 10
1
1
""") == "-1", "minimum impossible"

assert run("""1
4 4
2 2 2 2
2 2 2 2
""") == "3", "all equal"

assert run("""1
2 5
100 1
10 10
""") == "1", "tie on force but different masses"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single passenger that succeeds | `1` | Minimum feasible instance |
| Single passenger that fails | `-1` | Impossible instance |
| Four identical passengers | `3` | Correct prefix counting |
| Equal forces, different masses | `1` | Correct use of `mass + force` |

## Edge Cases

Consider the case where one passenger is overwhelmingly stronger than the others.

```
1
3 5
2 2 2
10 1 1
```

The target is `11`. The transformed values are `[12, 3, 3]`. After selecting the first value, the accumulated contribution is already `12`, so the algorithm immediately returns `1`. Choosing passengers by mass alone would miss this solution.

Now consider an impossible instance.

```
1
2 100
1 1
30 40
```

The target equals `102`, while the total contribution of every passenger is only `72`. The running sum never reaches the target, so the algorithm correctly returns `-1`.

Finally, examine passengers with equal force but different masses.

```
1
2 5
100 1
10 10
```

The transformed values are `[110, 11]`, and the target is `106`. The first value alone already reaches the target, so the answer is `1`. This demonstrates why both mass and force must be combined into a single contribution value rather than considering force alone.
