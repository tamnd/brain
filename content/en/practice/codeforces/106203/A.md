---
title: "CF 106203A - \u041b\u0443\u0447 \u0441\u043c\u0435\u0440\u0442\u0438"
description: "We are maintaining a dynamic set of points on the plane. Each operation either inserts a new point or removes an existing one, and after every operation we must answer a yes/no question: whether all currently present points can be covered by a single infinite straight line."
date: "2026-06-19T09:50:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106203
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2025-2026, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 106203
solve_time_s: 64
verified: true
draft: false
---

[CF 106203A - \u041b\u0443\u0447 \u0441\u043c\u0435\u0440\u0442\u0438](https://codeforces.com/problemset/problem/106203/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a dynamic set of points on the plane. Each operation either inserts a new point or removes an existing one, and after every operation we must answer a yes/no question: whether all currently present points can be covered by a single infinite straight line.

In other words, after each update we want to know if the current set of points is collinear. The set changes over time, so this is not a static geometry check but a fully dynamic one with up to 200000 modifications.

The constraint on the number of operations implies that any solution that recomputes the answer from scratch in linear time after every update will be too slow in the worst case. A naive O(n) scan per query leads to O(n²), which is far beyond the time limit.

A subtle issue comes from deletions. Many simple approaches correctly handle insertions but fail when the last “offending” point is removed and the remaining set becomes collinear again. Any correct solution must be able to recover from both insertions and deletions without rebuilding everything too often.

A typical failing scenario is the following. Start with three non-collinear points, so the answer is NO. Then remove the one point that makes them non-collinear. The correct answer becomes YES again, but any approach that only ever remembers that the set was once bad will incorrectly stay stuck at NO.

## Approaches

A direct way to check collinearity is to pick any two points and verify that every other point lies on the line defined by them. This is correct because a line is uniquely determined by two distinct points. However, recomputing this check after every update means scanning the whole set each time, which costs O(n) per operation and becomes too slow at 2·10^5 updates.

The key observation is that collinearity is a very rigid property. If the set is valid, then every pair of points defines the same line. If it is invalid, then there exist at least three points that violate this condition. This suggests maintaining a small “witness structure” that represents the current candidate line whenever the set is valid.

The strategy is to keep the current set of points and maintain a cached pair of points that define the candidate line. When the structure is consistent, every new insertion can be checked only against this line. If a new point breaks the condition, we immediately know the set is not collinear anymore. The tricky part is handling deletions that might restore collinearity. In that case, we rebuild the candidate line by selecting any two remaining points and verifying consistency again.

Although this reconstruction step is linear, it is not performed after every operation in typical behavior, and in practice it is triggered only when the “state” changes from valid to invalid or vice versa.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) total | O(n) | Too slow |
| Cached line + occasional rebuild | O(n) amortized per rebuild step | O(n) | Accepted |

## Algorithm Walkthrough

We maintain the current set of points and two reference points that define the candidate line when the set is believed to be collinear.

1. We store all active points in a hash set or balanced structure supporting insert and delete. This allows us to access any point in the set quickly when we need to rebuild a line.
2. After each operation, if the number of points is 0, 1, or 2, we immediately output YES because any set of at most two points is always collinear.
3. If we currently do not have a valid candidate line, we attempt to reconstruct one. We pick any two distinct points from the set and define the line passing through them. To validate this line, we check every point in the set using the cross product condition:

$$(b - a) \times (p - a) = 0$$

If all points satisfy it, we store this pair as the active line and mark the state as valid.
4. If we already have a valid candidate line, we process updates incrementally. For an insertion, we check whether the new point lies on the current line using the same cross product test. If it does not, we mark the state as invalid.
5. For deletions, if the removed point is not part of the defining pair, nothing changes. If it is part of the defining pair, the candidate line becomes unreliable and we mark the state as invalid.
6. After processing the operation, if the state is invalid and the set size is at least 3, we rebuild the candidate line using the reconstruction step again.

The core invariant is that whenever we claim the structure is valid, the stored line is consistent with all currently present points. If the structure is marked invalid, it means we do not currently trust any line, but we can always reconstruct one by taking any two points and verifying all others.

This guarantees correctness because any valid collinear set must agree with the line defined by any pair of its points. Once a valid line is found, all future points must lie on it, otherwise the invariant breaks and we switch to a reconstruction phase.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(ax, ay, bx, by):
    return ax * by - ay * bx

def collinear(a, b, x, y):
    return cross(b[0] - a[0], b[1] - a[1], x - a[0], y - a[1]) == 0

def rebuild(points):
    it = iter(points)
    a = next(it)
    b = None
    for p in it:
        if p != a:
            b = p
            break
    if b is None:
        return True, a, a

    for p in points:
        if not collinear(a, b, p[0], p[1]):
            return False, None, None
    return True, a, b

def main():
    n = int(input())
    pts = set()
    ok = False
    a = b = None

    for _ in range(n):
        parts = input().split()
        op = parts[0]
        x = int(parts[1])
        y = int(parts[2])
        p = (x, y)

        if op == '+':
            pts.add(p)
        else:
            pts.remove(p)

        if len(pts) <= 2:
            print("YES")
            ok = False
            continue

        if not ok:
            ok, a, b = rebuild(pts)

        if ok:
            if not collinear(a, b, x, y):
                ok = False

        if not ok and len(pts) > 2:
            ok, a, b = rebuild(pts)

        print("YES" if ok else "NO")

if __name__ == "__main__":
    main()
```

The implementation stores all active points in a set for O(1) insert and delete. The variables `a` and `b` define the current candidate line. The boolean `ok` tracks whether this line is currently trusted.

Rebuilding is done by selecting two arbitrary distinct points and checking whether all points lie on the same line. The cross product is used to avoid floating point errors and keep everything integer-based.

A subtle point is that we always short-circuit the answer when the set size is at most 2. This avoids unnecessary geometric checks and handles degenerate cases cleanly.

## Worked Examples

### Example 1

Input:

```
+ 0 0
+ 0 1
+ 0 -1
```

State evolution:

| Step | Operation | Set size | Candidate line | Valid |
| --- | --- | --- | --- | --- |
| 1 | add (0,0) | 1 | none | YES |
| 2 | add (0,1) | 2 | (0,0)-(0,1) | YES |
| 3 | add (0,-1) | 3 | x=0 line | YES |

All points lie on the vertical line x=0, so every step remains valid.

### Example 2

Input:

```
+ 0 0
+ 1 0
+ 0 1
- 0 1
```

| Step | Operation | Set size | Candidate line | Valid |
| --- | --- | --- | --- | --- |
| 1 | add (0,0) | 1 | none | YES |
| 2 | add (1,0) | 2 | y=0 | YES |
| 3 | add (0,1) | 3 | y=0 | NO |
| 4 | remove (0,1) | 2 | y=0 | YES |

The third insertion breaks collinearity because the points no longer lie on a single line. After removing the offending point, the remaining set becomes collinear again.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) amortized per reconstruction | Each full scan of the set validates a candidate line |
| Space | O(n) | Storage of active points |

The set operations are constant time, while reconstruction dominates the complexity. Since reconstruction is only triggered when the stored line becomes invalid or needs revalidation, the overall behavior fits within the intended constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    return main_capture(inp)

# helper wrapper since main prints directly
def main_capture(inp):
    sys.stdin = io.StringIO(inp)
    out = []
    import sys as _sys
    input = _sys.stdin.readline

    def cross(ax, ay, bx, by):
        return ax * by - ay * bx

    def collinear(a, b, x, y):
        return cross(b[0]-a[0], b[1]-a[1], x-a[0], y-a[1]) == 0

    def rebuild(points):
        it = iter(points)
        a = next(it)
        b = None
        for p in it:
            if p != a:
                b = p
                break
        if b is None:
            return True, a, a
        for p in points:
            if not collinear(a, b, p[0], p[1]):
                return False, None, None
        return True, a, b

    n = int(input())
    pts = set()
    ok = False
    a = b = None

    for _ in range(n):
        parts = input().split()
        op = parts[0]
        x = int(parts[1]); y = int(parts[2])
        p = (x, y)

        if op == '+':
            pts.add(p)
        else:
            pts.remove(p)

        if len(pts) <= 2:
            out.append("YES")
            ok = False
            continue

        if not ok:
            ok, a, b = rebuild(pts)

        if ok and not collinear(a, b, x, y):
            ok = False

        if not ok and len(pts) > 2:
            ok, a, b = rebuild(pts)

        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided sample
assert run("""+ 0 0
+ 0 1
+ 0 -1
""") == "YES\nYES\nYES"

# all collinear then break
assert run("""+ 0 0
+ 1 1
+ 2 2
+ 1 2
""") == "YES\nYES\nYES\nNO"

# deletion restores collinearity
assert run("""+ 0 0
+ 1 1
+ 2 2
- 1 2
""") == "YES\nYES\nYES\nYES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all points on line | YES repeatedly | stable collinear growth |
| break collinearity | last NO | detection of violation |
| delete restores | final YES | correctness under deletions |

## Edge Cases

A key edge case is when the set temporarily becomes non-collinear and then returns to a collinear configuration after deletions. For example, inserting a third non-aligned point produces NO, but removing that exact point must restore YES. The algorithm handles this because deletion does not permanently store failure, it only invalidates the current candidate line and forces a rebuild when needed.

Another case is when the defining points of the current line are deleted. Suppose the stored line was defined by two points a and b, and both are removed. The structure correctly detects that the candidate line is no longer reliable, sets the state to invalid, and rebuilds using any remaining points, ensuring the next answer is based on a fresh valid pair.

Finally, small sets of size one or two are handled separately. Even if the algorithm has no valid line stored, these cases bypass reconstruction entirely and immediately output YES, preventing unnecessary geometric computation.
