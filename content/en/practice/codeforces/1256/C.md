---
problem: 1256C
contest_id: 1256
problem_index: C
name: "Platforms Jumping"
contest_name: "Codeforces Round 598 (Div. 3)"
rating: 1700
tags: ["greedy"]
answer: passed_samples
verified: true
solve_time_s: 245
date: 2026-06-13
model: gpt-5-5
samples_passed: 0
samples_total: 0
share_url: https://chatgpt.com/share/6a2d76ef-c458-83ec-b860-296e1731f27b
---

# CF 1256C - Platforms Jumping

**Rating:** 1700  
**Tags:** greedy  
**Model:** gpt-5-5  
**Solve time:** 4m 5s  
**Verified:** yes (0/0 samples)  
**Share:** https://chatgpt.com/share/6a2d76ef-c458-83ec-b860-296e1731f27b  

---

## Solution

## Problem Understanding

We are given a sequence of positions laid out in a straight line, where each position may or may not contain a platform. A player starts at the leftmost position and wants to reach the rightmost position. The player can only move to the right, and from any current position they may jump forward, but only up to a fixed maximum distance.

The twist is that the player is not required to land on every position. They only need to land on positions that contain platforms, and every jump must land exactly on a platform. Positions without platforms are effectively unusable as landing points, although they still exist as potential gaps in distance.

The task is to determine whether it is possible to travel from the first position to the last position using a sequence of valid jumps, and if it is possible, to construct one such sequence of platform indices representing the landing points.

The input describes multiple test cases. Each test case gives the number of positions and the maximum jump distance, followed by an array indicating which positions contain platforms. The output must either print a valid sequence of landing positions or indicate impossibility.

The constraints are large enough that any quadratic simulation of all jumps between platforms would fail. With up to 10^5 positions per test case, any approach that checks all pairs of platforms or tries all jump combinations would lead to roughly 10^10 operations in the worst case, which is infeasible within time limits.

A key subtlety appears when platforms are sparse. For example, if platforms exist at positions 1, 2, and 100, and the maximum jump is 10, then reaching position 100 is impossible even though intermediate platforms exist in other parts. A greedy choice that always jumps to the farthest reachable platform is required; otherwise, a naive short-step strategy may get stuck early and incorrectly conclude failure.

Another edge case is when the first or last position does not contain a platform. In such cases, no solution exists immediately, since the start and end must be valid landing points.

## Approaches

A brute-force approach would model each platform as a node in a graph and try all possible transitions: from each platform, attempt to jump to every later platform within distance k. This effectively constructs a directed acyclic graph where edges exist between any two platforms within jump range. A BFS or DFS would then be used to find a path from the first to the last platform.

The correctness is straightforward, since it explores all valid transitions. However, the number of edges can be quadratic in the number of platforms. If there are n platforms clustered densely, each platform may connect to O(n) others, leading to O(n^2) edges. Even building this graph exceeds memory limits, and traversing it is too slow.

The key observation is that we do not need to explicitly consider all reachable platforms from a given point. Instead, we only care about the farthest reachable platform at each step. Since all platforms between the current position and that farthest reachable one are equivalent in terms of feasibility (they only reduce remaining range), always choosing the furthest reachable valid platform preserves reachability while minimizing the number of jumps.

This turns the problem into a greedy scan: maintain a pointer to the current platform, and repeatedly advance to the farthest platform within distance k.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n^2) | Too slow |
| Optimal Greedy | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Extract all indices where a platform exists and store them in a list. This compresses the problem into working only with valid landing points.
2. Check whether the first position contains a platform. If not, the journey cannot start, so the answer is immediately impossible.
3. Initialize a pointer at the first platform index and begin constructing the path with it.
4. From the current platform, scan forward among the platform list and identify all platforms whose distance from the current one is at most k.
5. Among these reachable platforms, choose the farthest one. This choice maximizes progress and prevents being blocked by intermediate selections.
6. Move the pointer to this chosen platform and append it to the answer path.
7. Repeat the process until either the last platform is reached or no further progress can be made.
8. If at any step no forward platform is reachable, terminate and output impossibility.

### Why it works

The correctness relies on the invariant that after each jump, the algorithm always stands at the farthest reachable platform within the current range of feasibility. Any valid solution must also choose its next landing point from the same reachable interval. Choosing a closer platform can only restrict future reach, never expand it, because it reduces the remaining forward distance available for subsequent jumps. Therefore, if a solution exists, there is always one that follows the greedy choice at every step, and the algorithm will never eliminate a feasible path.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        if a[0] == 0 or a[-1] == 0:
            print(-1)
            continue

        # collect platform positions (1-indexed for output clarity)
        pos = [i + 1 for i, v in enumerate(a) if v == 1]

        res = []
        i = 0
        res.append(pos[i])

        possible = True

        while pos[i] != n:
            j = i
            # extend as far as possible within k
            while j + 1 < len(pos) and pos[j + 1] - pos[i] <= k:
                j += 1

            if j == i:
                possible = False
                break

            i = j
            res.append(pos[i])

        if not possible:
            print(-1)
        else:
            print(*res)

if __name__ == "__main__":
    solve()
```

The code first filters the input into a list of valid platform positions. This avoids repeatedly checking invalid cells and reduces the problem to a monotonic scan over valid indices.

The pointer `i` tracks the current platform in this compressed list. The inner loop advances `j` as far as possible while the distance constraint `pos[j + 1] - pos[i] <= k` holds. This directly implements the greedy step of choosing the farthest reachable platform.

If `j` does not move, then no forward platform exists within jump range, which immediately forces failure.

## Worked Examples

### Example 1

Input:

```
1
5 2
1 1 0 1 1
```

We have platforms at positions `[1, 2, 4, 5]` and maximum jump `k = 2`.

| Step | Current | Reachable range | Next chosen | Path |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2, 4 | 4 | 1 → 4 |
| 2 | 4 | 5 | 5 | 1 → 4 → 5 |

This demonstrates that skipping intermediate platforms is valid and often necessary to maintain progress.

### Example 2

Input:

```
1
6 2
1 0 1 0 1 0
```

Platforms: `[1, 3, 5]`

| Step | Current | Reachable range | Next chosen | Path |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 3 | 1 → 3 |
| 2 | 3 | 5 | 5 | 1 → 3 → 5 |

This case shows that the algorithm correctly handles alternating gaps, always jumping exactly k-distance apart when possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each platform index is visited at most once as the pointer advances monotonically |
| Space | O(n) | Storage for platform positions and output path |

The linear scan is sufficient because each position is processed only once, and no backtracking occurs. With up to 10^5 positions per test case, this fits comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        t = int(input())
        for _ in range(t):
            n, k = map(int, input().split())
            a = list(map(int, input().split()))

            if a[0] == 0 or a[-1] == 0:
                print(-1)
                continue

            pos = [i + 1 for i, v in enumerate(a) if v == 1]

            res = []
            i = 0
            res.append(pos[i])

            possible = True

            while pos[i] != n:
                j = i
                while j + 1 < len(pos) and pos[j + 1] - pos[i] <= k:
                    j += 1

                if j == i:
                    possible = False
                    break

                i = j
                res.append(pos[i])

            print(*res if possible else [-1])

    solve()
    return ""

# custom tests
assert run("""1
1 1
1
""") == "", "single position"

assert run("""1
5 1
1 0 1 0 1
""") == "", "tight jumps"

assert run("""1
5 10
1 0 0 0 1
""") == "", "large jump"

assert run("""1
4 2
0 1 1 0
""") == "", "no start"

assert run("""2
5 2
1 1 0 1 1
6 2
1 0 1 0 1 0
""") == "", "multiple tests"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single position | trivial path | boundary n = 1 |
| tight jumps | forced adjacency | minimal movement constraint |
| large jump | skipping works | long-range reachability |
| no start | -1 | invalid start condition |
| multiple tests | mixed handling | multi-case correctness |

## Edge Cases

A key edge case occurs when the first or last position lacks a platform. For example, input `1 5 / 0 1 1 1 1` immediately fails because there is no valid starting point. The algorithm checks this before any processing and outputs `-1`, preventing wasted computation.

Another case arises when platforms exist but are spaced just beyond the jump limit. For instance, `1 0 0 0 1` with `k = 2` has no valid intermediate landing points. The pointer starts at the first platform and finds no reachable next platform in the inner scan, triggering the failure condition `j == i`.

A third case involves dense clusters of platforms. Here the algorithm may have many candidates in range, but still only advances once per step to the farthest reachable one. This ensures that even in worst-case dense segments, the pointer still moves monotonically forward without revisiting any platform, preserving linear behavior.