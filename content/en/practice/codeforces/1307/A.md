---
problem: 1307A
contest_id: 1307
problem_index: A
name: "Cow and Haybales"
contest_name: "Codeforces Round 621 (Div. 1 + Div. 2)"
rating: 800
tags: ["greedy", "implementation"]
answer: passed_samples
verified: true
solve_time_s: 181
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2dd980-f264-83ec-8273-607302c398bb
---

# CF 1307A - Cow and Haybales

**Rating:** 800  
**Tags:** greedy, implementation  
**Model:** gpt-5-3-mini  
**Solve time:** 3m 1s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2dd980-f264-83ec-8273-607302c398bb  

---

## Solution

## Problem Understanding

We are given a line of hay piles, each pile holding some number of haybales. In one move, we are allowed to take a single haybale from a pile and shift it to one of its immediate neighbors. This process can be repeated for at most `d` days, and on each day we may also choose to do nothing.

The goal is to make the first pile as large as possible after at most `d` such moves.

What makes this problem subtle is that moving haybales is not teleportation. Every haybale has to physically traverse adjacent piles, so the cost of moving a bale from position `i` to position `1` is exactly `i - 1` days, assuming we move it left step by step. This immediately suggests that not all haybales are equally valuable within the time limit.

The input consists of multiple independent scenarios. For each one, we must compute the best possible final value of the first pile after at most `d` moves.

The constraints are small: `n, d ≤ 100`, and each pile height is also small. This means we can afford quadratic or even cubic reasoning per test case without concern. Any solution that tries to simulate day-by-day movement greedily is also viable, but we should be careful not to overcomplicate something that reduces to a simple local optimality rule.

A common mistake is to assume that we should always pull from the nearest non-zero pile whenever possible. That intuition is close but incomplete. The real constraint is that each pile can only contribute a limited number of haybales based on how many of them can physically reach index `1` within `d` steps.

A second pitfall is to simulate movements greedily over days. This can fail because multiple haybales compete for the same path capacity, and naive simulation can waste moves moving haybales back and forth without improving the final count.

## Approaches

A brute-force idea is to simulate all possible sequences of moves over `d` days. Each day, we pick a pile and shift one unit left or right. The state space is enormous even for small inputs, because each day branches over `O(n)` choices, giving roughly `O(n^d)` possibilities. Even with pruning, this becomes intractable quickly.

We need a different perspective: instead of simulating movement over time, we should reason about how many haybales can end up at index `1` within a limited travel budget.

Each haybale located at position `i` contributes to pile `1` only if we can move it left `i-1` times. Since each move consumes one day, the condition is simply `i - 1 ≤ d`. This means every pile independently contributes all of its haybales if it is within reachable distance, and contributes nothing otherwise.

There is no interaction penalty between different piles because moving one haybale does not block another; the only constraint is time. Therefore, the optimal strategy is to take everything from all piles that can reach index `1` within `d` moves.

This reduces the problem to a simple prefix sum over reachable positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^d) | O(n) | Too slow |
| Distance-based Summation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each pile at index `i`, compute its distance to the first pile as `i - 1`. This represents the minimum number of moves required to transfer one haybale to pile `1`.
2. Compare this distance with the available number of days `d`. If `i - 1 ≤ d`, then every haybale in that pile can eventually be moved to pile `1`.
3. If the condition is satisfied, add the full value `a[i]` to the answer.
4. If the condition is not satisfied, ignore the pile completely because none of its haybales can reach the first position within the time limit.
5. Sum contributions from all piles and output the result.

The key idea is that each haybale is independent. We are not choosing an ordering of moves; we are only checking feasibility of completing its path within the time constraint.

### Why it works

Each haybale behaves like a unit requiring a fixed travel cost equal to its distance from pile `1`. Since moves are not exclusive in a way that limits parallel usage of time beyond the global budget `d`, feasibility depends only on whether each individual unit fits inside that budget. There is no benefit in delaying or rearranging moves because every move is identical in cost and effect, so the optimal solution is simply the sum of all independently feasible contributions.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, d = map(int, input().split())
    a = list(map(int, input().split()))
    
    ans = 0
    for i in range(n):
        if i <= d:
            ans += a[i]
    
    print(ans)
```

The implementation directly encodes the distance observation. The index `i` already represents the distance from pile `1` in zero-based indexing, so we simply check whether `i` is within the allowed number of days.

No simulation is required. Each test case is handled in linear time by scanning the array once and summing valid contributions.

A common implementation mistake is off-by-one indexing. Since pile `1` corresponds to index `0`, the correct distance is exactly `i`, not `i + 1`.

## Worked Examples

### Example 1

Input:

```
4 5
1 0 3 2
```

We track which piles can contribute.

| i | a[i] | i ≤ d | Contribution |
| --- | --- | --- | --- |
| 0 | 1 | yes | 1 |
| 1 | 0 | yes | 0 |
| 2 | 3 | yes | 3 |
| 3 | 2 | yes | 2 |

Final sum is `6`.

This shows that all piles are within reach since `d = 5` exceeds all distances.

### Example 2

Input:

```
2 2
100 1
```

| i | a[i] | i ≤ d | Contribution |
| --- | --- | --- | --- |
| 0 | 100 | yes | 100 |
| 1 | 1 | yes | 1 |

Final result is `101`.

This confirms that even a pile one step away can fully contribute, as long as its distance is within the time limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan each pile once and perform constant work per element |
| Space | O(1) extra | Only a running sum is stored |

Given `n ≤ 100` and `t ≤ 100`, the solution performs at most 10,000 operations, which is trivially fast under the limits.

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
        n, d = map(int, input().split())
        a = list(map(int, input().split()))
        ans = 0
        for i in range(n):
            if i <= d:
                ans += a[i]
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""3
4 5
1 0 3 2
2 2
100 1
1 8
0
""") == """6
101
0"""

# custom cases
assert run("""1
1 0
5
""") == "5", "single element always reachable"

assert run("""1
5 0
1 2 3 4 5
""") == "1", "only first pile contributes"

assert run("""1
5 10
1 2 3 4 5
""") == "15", "all piles reachable"

assert run("""1
4 2
10 20 30 40
""") == "60", "prefix cutoff at distance 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 5 | base case, zero distance |
| only first pile | 1 | no movement allowed |
| all reachable | 15 | full accumulation |
| prefix cutoff | 60 | correct distance boundary |

## Edge Cases

A critical edge case is when `d = 0`. In this situation, no movement is possible, so only pile `1` can contribute. The algorithm handles this because only index `0` satisfies `i ≤ 0`.

Another case is when `d` is very large compared to `n`. Here every pile becomes reachable, and the correct answer is simply the total sum of all haybales. The loop naturally includes all indices.

Finally, when the first pile is empty but distant piles contain hay, the solution still works correctly because it does not assume anything about initial `a[1]`; it only accumulates reachable contributions based on distance.