---
problem: 900A
contest_id: 900
problem_index: A
name: "Find Extra One"
contest_name: "Codeforces Round 450 (Div. 2)"
rating: 800
tags: ["geometry", "implementation"]
answer: passed_samples
verified: true
solve_time_s: 59
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
---

# CF 900A - Find Extra One

**Rating:** 800  
**Tags:** geometry, implementation  
**Model:** gpt-5-3-mini  
**Solve time:** 59s  
**Verified:** yes (1/1 samples)  

---

## Solution

## Problem Understanding

We are given a set of points in the plane, and none of them lie on the vertical axis. This means every point is either strictly to the left of the y-axis or strictly to the right of it. The task is to check whether we can delete exactly one point so that all remaining points end up entirely on one side of the y-axis, meaning all remaining x-coordinates are either strictly positive or strictly negative.

So the core question is not about geometry in a deep sense, but about whether the set becomes “one-sided” after removing a single outlier point.

The input size allows up to 100000 points, which rules out any quadratic strategy like trying every removal and checking the rest directly in O(n) each time. That would lead to about 10^10 operations in the worst case, which is too slow for a one second limit. We need a linear or near-linear scan.

The key subtlety is that the answer depends only on how many points are on the left side (x < 0) and how many are on the right side (x > 0). The y-coordinates are irrelevant for the condition.

A common mistake is to think spatial structure matters beyond the sign of x. For example, someone might try sorting or checking convexity, but none of that affects whether all remaining points lie strictly on one side of the y-axis.

Edge cases appear when both sides are populated in a balanced way. For instance, if there are two points on each side, removing one point still leaves both sides represented, so it is impossible.

Another subtle case is when all points are already on one side. For example:

Input:

```
3
1 2
3 4
5 6
```

This is already valid, since removing any one point keeps all remaining points on the positive side.

A naive mistake is to assume we must remove a point that changes the side distribution, but the condition is already satisfied without any special structure.

## Approaches

A brute-force approach would try removing each point in turn, then scanning all remaining points to check whether all x-values share the same sign. For each of the n candidates, we would do another O(n) scan, leading to O(n^2) time complexity. With n up to 100000, this becomes about 10^10 checks, which is not feasible.

The key observation is that the condition after removing one point depends only on counts of negative and positive x-coordinates. After removal, we want either zero negatives or zero positives. That means we are allowed to “fix” at most one violation by removing one point.

So we compute how many points lie on each side. If both sides have at least two points, removing one point cannot eliminate both sides, so the answer is immediately “No”. If at least one side has zero points, the answer is already “Yes”. If one side has exactly one point, removing that single point resolves the issue, so answer is “Yes”.

This reduces the problem to a simple counting task.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal Counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all points and classify them by the sign of their x-coordinate. We only care whether x is positive or negative, not the exact value or y-coordinate.
2. Count how many points have x < 0 and how many have x > 0.
3. If all points are on one side already, return “Yes” because removing any single point preserves the property.
4. If both counts are greater than 1, return “No” because removing one point still leaves at least one point on each side.
5. Otherwise, return “Yes” because removing the single remaining point on one side eliminates that side entirely.

### Why it works

The only way to satisfy the condition after removal is to end up with all remaining points having the same sign of x. Removing one point can reduce the count of one side by at most one. So if both sides initially have at least two points, neither side can be eliminated completely by a single removal. Conversely, if at least one side has size zero or one, we can always remove a point to make the remaining set one-sided.

This gives a complete characterization of all valid configurations.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
neg = 0
pos = 0

for _ in range(n):
    x, y = map(int, input().split())
    if x < 0:
        neg += 1
    else:
        pos += 1

# already one-sided
if neg == 0 or pos == 0:
    print("Yes")
elif neg <= 1 or pos <= 1:
    print("Yes")
else:
    print("No")
```

The code directly implements the counting logic. The first condition handles the case where all points already lie on one side. The second condition captures the situation where one side can be completely eliminated by removing a single point.

No sorting or geometric computation is needed because only the sign of x matters.

## Worked Examples

### Example 1

Input:

```
3
1 1
-1 -1
2 -1
```

We track counts:

| Step | x | neg | pos |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 1 |
| 2 | -1 | 1 | 1 |
| 3 | 2 | 1 | 2 |

After processing, neg = 1, pos = 2.

Since one side has size 1, removing that point makes all remaining points on one side.

Output is “Yes”.

This confirms that a single outlier on the negative side can be removed.

### Example 2

Input:

```
4
-1 0
-2 1
1 3
2 5
```

| Step | x | neg | pos |
| --- | --- | --- | --- |
| 1 | -1 | 1 | 0 |
| 2 | -2 | 2 | 0 |
| 3 | 1 | 2 | 1 |
| 4 | 2 | 2 | 2 |

Now neg = 2 and pos = 2.

Removing one point still leaves at least one point on both sides, so it is impossible to make all points one-sided.

Output is “No”.

This demonstrates the critical threshold where both sides are too large to fix with a single removal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass counting x-signs |
| Space | O(1) | Only two counters are stored |

The solution performs one scan over at most 100000 points, which is comfortably within time limits. Memory usage is constant and independent of input size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from collections import deque

    data = inp.strip().split()
    it = iter(data)
    n = int(next(it))
    neg = 0
    pos = 0
    for _ in range(n):
        x = int(next(it))
        y = int(next(it))
        if x < 0:
            neg += 1
        else:
            pos += 1
    return "Yes\n" if (neg == 0 or pos == 0 or neg <= 1 or pos <= 1) else "No\n"

# provided sample 1
assert run("""3
1 1
-1 -1
2 -1
""") == "Yes\n"

# sample 2 (constructed)
assert run("""4
-1 0
-2 1
1 3
2 5
""") == "No\n"

# all positive
assert run("""3
1 1
2 2
3 3
""") == "Yes\n"

# all negative
assert run("""3
-1 1
-2 2
-3 3
""") == "Yes\n"

# borderline case: one negative
assert run("""3
-1 1
1 2
2 3
""") == "Yes\n"

# borderline case: two and two
assert run("""4
-1 0
-2 0
1 0
2 0
""") == "No\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all positive | Yes | already valid one side |
| all negative | Yes | symmetric case |
| one negative, rest positive | Yes | single removal fixes |
| two and two split | No | cannot fix with one removal |

## Edge Cases

One important edge case is when all points already lie on one side. For example, if every x is positive, the algorithm counts neg = 0 and pos = n. The condition `neg == 0 or pos == 0` triggers immediately, and the output is “Yes”. This matches the fact that removing any point preserves the one-sided property.

Another edge case is when exactly one point lies on one side. For instance:

Input:

```
3
-1 2
1 3
2 4
```

The counts become neg = 1 and pos = 2. The condition `neg <= 1` is true, so we can remove the single negative point and leave only positive points. The algorithm correctly identifies this without simulating removals.

The final edge case is when both sides have at least two points. For example:

```
4
-1 0
-2 0
1 0
2 0
```

Here neg = 2 and pos = 2. None of the acceptance conditions are met, so the output is “No”. Any removal still leaves at least one point on each side, so it is impossible to satisfy the requirement with a single deletion.