---
problem: 1294B
contest_id: 1294
problem_index: B
name: "Collecting Packages"
contest_name: "Codeforces Round 615 (Div. 3)"
rating: 1200
tags: ["implementation", "sortings"]
answer: passed_samples
verified: true
solve_time_s: 260
date: 2026-06-14
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2dc44f-5540-83ec-8334-913517db904d
---

# CF 1294B - Collecting Packages

**Rating:** 1200  
**Tags:** implementation, sortings  
**Model:** gpt-5-5  
**Solve time:** 4m 20s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2dc44f-5540-83ec-8334-913517db904d  

---

## Solution

## Problem Understanding

A robot starts at the origin of a grid and can only move in two directions: right or up. Each package is located at a distinct grid coordinate with non-negative integer values. The robot must visit all package locations starting from the origin, and it is allowed to choose the visiting order freely. Each move increments either the x-coordinate or the y-coordinate by one.

The task is to determine whether there exists an order of visiting all points such that the robot never needs to move left or down while still being able to reach every package in that order. If such an order exists, we must construct a valid shortest path string of moves. Among all shortest valid paths, we must output the lexicographically smallest one, where 'R' is considered smaller than 'U'.

The constraints make the solution very tightly bound to linear or near-linear sorting logic. The total number of points across all test cases is at most 1000, so an O(n log n) sorting strategy is easily sufficient. Anything involving permutations or backtracking over all orders would explode combinatorially and is immediately infeasible beyond very small n.

A subtle issue appears when points are “incompatible” in terms of monotone traversal. For example, if we have points (1, 2) and (2, 1), no monotone path can visit both in a single increasing sequence of x and y moves without violating monotonicity. Any attempt to force an order will eventually require a downward or leftward move, which is disallowed.

A naive mistake is trying to sort points only by x or only by y. For instance, sorting only by x could produce a sequence where y decreases between consecutive points, making a direct monotone traversal impossible. Similarly, arbitrary ordering of points leads to invalid intermediate states where the robot would need to “go back”.

## Approaches

A brute-force idea is to try all permutations of the points, check whether each ordering can be traversed using only right and up moves, and track the best lexicographically smallest path among valid ones. For each permutation, we simulate moving from (0,0) to the first point, then between consecutive points, verifying that both coordinates never decrease. This works because it explicitly enforces feasibility, but it requires checking n! orders, and even for n = 10 this already becomes computationally infeasible.

The key structural observation is that any valid path must move in a non-decreasing x and non-decreasing y fashion. This means that once we commit to visiting a point with larger x, we can never later visit a point with smaller x. The same applies to y in relative ordering constraints between consecutive points.

This suggests that if we sort points by x-coordinate and process them in increasing order, we automatically guarantee that we never need to move left. The only remaining problem is whether within equal x-values we can maintain feasibility. For lexicographically smallest output, we want to prefer moves that produce 'R' as early as possible, which aligns with prioritizing smaller x transitions before y transitions.

However, the crucial refinement is that we do not actually need to enforce strict ordering among points themselves. Instead, we only care that when moving from current position to the next target, we can only move right and up, meaning both coordinates must be non-decreasing along the chosen sequence. Therefore, the optimal strategy is to sort points by x ascending, and for equal x, by y ascending. This ensures a monotone increasing chain in both dimensions, which guarantees feasibility.

Once this chain is fixed, constructing the path is straightforward: from the current position, move right until reaching the next x, then up until reaching the next y. Because x never decreases and y never decreases, this always works.

The lexicographically smallest requirement is naturally satisfied because we always exhaust all required 'R' moves before 'U' moves at each stage when possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Sort by coordinates | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct a valid path by enforcing a monotone progression through sorted points.

1. Read all package coordinates for the test case. These represent target cells the robot must reach.
2. Sort all points by increasing x-coordinate, and for equal x, by increasing y-coordinate. This ensures that when moving through the list, both coordinates never decrease, so no backward movement is ever required.
3. Initialize current position at (0, 0) and an empty result string.
4. Iterate through the sorted points. For each point (x, y), move horizontally from the current x to x using 'R' steps, then vertically from the current y to y using 'U' steps. Append these moves to the answer string. This ordering is forced because moving right first preserves lexicographic minimality.
5. After processing all points, output the constructed path.

Why it works

The sorted order guarantees that both x and y are non-decreasing along the sequence of visited points. This ensures that every transition between consecutive points is achievable using only right and up moves. Since we always complete all horizontal movement before vertical movement, we produce the smallest possible string in lexicographic order among all valid monotone paths, because any attempt to insert a 'U' earlier would delay a necessary 'R' and produce a lexicographically larger prefix.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    
    pts.sort()
    
    x, y = 0, 0
    res = []
    ok = True
    
    for nx, ny in pts:
        if nx < x or ny < y:
            ok = False
            break
        
        res.append('R' * (nx - x))
        res.append('U' * (ny - y))
        x, y = nx, ny
    
    if not ok:
        print("NO")
    else:
        print("YES")
        print(''.join(res))
```

The code begins by sorting the points lexicographically, which corresponds to sorting by x then y. This guarantees the monotone property required for feasibility checking. We maintain a pointer for the robot’s current position and incrementally construct the path by adding exactly the number of right and up moves needed to reach each successive point.

The validity check ensures we never attempt to move backward. If any point violates monotonicity relative to the previous one, the construction fails.

The construction order is crucial: we always append all required 'R' moves before 'U' moves, which is what ensures lexicographic minimality among valid monotone paths.

## Worked Examples

### Example 1

Input points: (1,3), (1,2), (3,3)

After sorting, we get: (1,2), (1,3), (3,3)

| Step | Current (x,y) | Target (x,y) | R moves | U moves | Path |
| --- | --- | --- | --- | --- | --- |
| 1 | (0,0) | (1,2) | R | UU | RUU |
| 2 | (1,2) | (1,3) |  | U | RUUU |
| 3 | (1,3) | (3,3) | RR |  | RUUURR |

This trace shows that sorting resolves the seemingly “unsorted” input into a monotone chain. The robot never needs to decrease coordinates, confirming feasibility.

### Example 2

Input points: (1,0), (0,1)

After sorting: (0,1), (1,0)

| Step | Current | Target | Valid transition |
| --- | --- | --- | --- |
| 1 | (0,0) | (0,1) | U |
| 2 | (0,1) | (1,0) | invalid (y decreases) |

This immediately fails because y would need to decrease from 1 to 0. The algorithm correctly outputs NO.

This demonstrates that sorting alone is not sufficient unless monotonic feasibility holds, which the check enforces.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, each test processes points linearly afterward |
| Space | O(n) | Stores all points and output string |

The total number of points across all test cases is at most 1000, so sorting and linear construction easily fit within the time limit.

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
        pts = [tuple(map(int, input().split())) for _ in range(n)]
        pts.sort()

        x, y = 0, 0
        res = []
        ok = True

        for nx, ny in pts:
            if nx < x or ny < y:
                ok = False
                break
            res.append('R' * (nx - x))
            res.append('U' * (ny - y))
            x, y = nx, ny

        out.append("NO" if not ok else "YES\n" + ''.join(res))

    return "\n".join(out)

# provided samples
assert run("""3
5
1 3
1 2
3 3
5 5
4 3
2
1 0
0 1
1
4 3
""") == """YES
RUUURRRRUU
NO
YES
RRRRUUU"""

# minimum size
assert run("""1
1
0 0
""") == """YES
"""

# simple monotone chain
assert run("""1
3
0 1
1 1
1 2
""") == """YES
URRU"""

# impossible case
assert run("""1
2
1 0
0 1
""") == """NO"""

# large increasing chain
assert run("""1
3
0 0
1 0
2 0
""") == """YES
RR"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single (0,0) | YES | trivial base case |
| monotone chain | YES URRU | correct construction order |
| (1,0),(0,1) | NO | infeasible ordering detection |
| horizontal chain | YES RR | pure R handling |

## Edge Cases

A single package at (0,0) is handled cleanly because no movement is needed and the sorted sequence remains valid. The output is simply YES with an empty path, matching the requirement that the robot is already at that location.

Two points that require crossing in opposite diagonal directions, such as (1,0) and (0,1), fail immediately because sorting produces a step that requires decreasing a coordinate. The check catches this before any path construction, ensuring correctness.

Cases where all points lie on a single increasing line, such as (0,0), (1,0), (2,0), demonstrate that the algorithm degenerates to a pure sequence of 'R' moves without unnecessary complexity, confirming optimality of the construction.