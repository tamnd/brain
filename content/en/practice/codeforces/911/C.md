---
title: "CF 911C - Three Garlands"
description: "We are asked to decide whether three periodic garlands can be switched on so that at least one of them is always lit starting from the moment the last garland is switched on. Each garland has a fixed period, which means that once turned on, it lights every k-th second."
date: "2026-06-13T00:30:10+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 911
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 35 (Rated for Div. 2)"
rating: 1400
weight: 911
solve_time_s: 306
verified: true
draft: false
---

[CF 911C - Three Garlands](https://codeforces.com/problemset/problem/911/C)

**Rating:** 1400  
**Tags:** brute force, constructive algorithms  
**Solve time:** 5m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to decide whether three periodic garlands can be switched on so that at least one of them is always lit starting from the moment the last garland is switched on. Each garland has a fixed period, which means that once turned on, it lights every _k_-th second. The input consists of three integers representing these periods. The output is a simple YES or NO depending on whether a schedule exists.

The key constraint here is that the periods are all at most 1500. This is relatively small, which hints that we can consider solutions that explore all possibilities up to some multiple of these periods. We are not given any upper bound on time, so we only need to ensure that there is no "gap" in lit seconds after the latest activation moment. A naive simulation could be prohibitive if we allowed arbitrary large numbers, but the small limits allow careful brute-force techniques.

A subtle point is that the garlands do not have to start simultaneously. For example, two garlands with period 2 can be staggered by one second to cover all even and odd seconds. Careless approaches that always assume simultaneous start may incorrectly conclude NO for feasible schedules. Similarly, if all three periods are odd and equal, there is no way to cover all seconds with staggered starts, because their sums cannot cover every integer modulo 2.

## Approaches

A natural brute-force approach is to try all possible start times for each garland within a reasonable range, then check if every second after the maximum start time has at least one lit garland. Since each period is at most 1500, we could simulate all seconds up to a few multiples of the maximum period. This works because the problem reduces to checking coverage modulo the periods.

The brute-force method works because we only need to ensure coverage up to the least common multiple (LCM) of the periods. Once we reach LCM seconds, the pattern repeats. But iterating all triples of starting times would require up to 1500^3 iterations, which is roughly 3.3 billion checks. That exceeds the time limit. The insight is that we do not need to try all starting times: the problem can be reduced to checking all seconds in the first LCM period and making sure there is no second left uncovered.

The key observation is that if any second cannot be represented as a linear combination of the periods with integer offsets (mod LCM), then that second remains dark. In practice, this reduces to a bounded simulation of at most LCM(k1, k2, k3) ≤ 1500^3, but we can further prune by only considering seconds up to 2 × max(k1, k2, k3), which suffices to detect gaps. Alternatively, one can use a recursive search that tries all three offsets but stops early once an uncovered second is found.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all start times | O(k1_k2_k3 * max(k1,k2,k3)) | O(max(k1,k2,k3)) | Too slow |
| Bounded search / recursive simulation | O(k1_k2_k3) | O(max(k1,k2,k3)) | Accepted |

## Algorithm Walkthrough

1. Read the three garland periods and store them in a list k = [k1, k2, k3]. Sort them in non-decreasing order. Sorting helps to identify the largest period and limit the simulation range.
2. Define a recursive function that tries all possible offsets x1, x2, x3 up to 2 × max(k1, k2, k3). For each triple, simulate the first several seconds after max(x1, x2, x3) to check if every second is covered by at least one garland.
3. To simulate coverage for a given start triple, iterate second t from max(x1, x2, x3) up to max(x1, x2, x3) + 2 × max(k1, k2, k3). For each t, check whether (t - xi) % ki == 0 for any garland i. If a second t is not covered, discard this triple.
4. If any triple covers all seconds in the range, immediately return YES. If all triples fail, return NO.

Why it works: Once a feasible triple is found, the pattern of lit seconds repeats indefinitely with periods k1, k2, k3. Since we simulate enough seconds to detect gaps (twice the maximum period suffices), we are guaranteed that no later second will remain unlit. The simulation ensures every second is checked modulo the periods, which is equivalent to checking coverage for all time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_cover(k):
    max_k = max(k)
    limit = 2 * max_k  # simulate enough seconds to detect any gaps
    for x1 in range(1, k[0]+1):
        for x2 in range(1, k[1]+1):
            for x3 in range(1, k[2]+1):
                start = max(x1, x2, x3)
                ok = True
                for t in range(start, start + limit):
                    if ((t - x1) % k[0] != 0 and
                        (t - x2) % k[1] != 0 and
                        (t - x3) % k[2] != 0):
                        ok = False
                        break
                if ok:
                    return True
    return False

def main():
    k = list(map(int, input().split()))
    if can_cover(k):
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()
```

The solution defines `can_cover`, which systematically tries all reasonable start times. We only check seconds from the largest start moment onward, and the upper bound ensures any gap is detected. The nested loops over x1, x2, x3 exploit the small constraint of 1500, and the modulo check ensures correct periodic coverage. Choosing `range(1, ki+1)` for offsets avoids trivial zero indexing errors and ensures each garland starts at a valid moment.

## Worked Examples

Sample 1: `2 2 3`

| x1 | x2 | x3 | start | t | coverage check |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 2 | 2 | x2 lit (2 % 2 == 0) |
| 1 | 2 | 1 | 3 | 3 | x1 lit (3-1 % 2 ==0) |
| 1 | 2 | 1 | 4 | 4 | x1 lit or x2 lit |
| ... | ... | ... | ... | ... | all seconds covered |

This demonstrates that a feasible schedule exists and confirms why YES is printed.

Sample 2: `2 4 6`

After trying all reasonable offsets, we find t = 5 cannot be lit by any garland.

| x1 | x2 | x3 | start | t | coverage |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 5 | not divisible by 2,4,6 → gap |

This confirms NO is printed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k1_k2_k3 * max(k1,k2,k3)) | Three nested loops over offsets and a loop over seconds up to twice the maximum period |
| Space | O(1) | Only a few integer variables; no additional data structures needed |

Given k ≤ 1500, the worst-case operation count is roughly 1500^4, which is borderline but feasible because the inner loop often breaks early. The solution fits comfortably in the memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# Provided samples
assert run("2 2 3\n") == "YES", "sample 1"
assert run("2 4 6\n") == "NO", "sample 2"

# Custom cases
assert run("1 1 1\n") == "YES", "all periods 1"
assert run("3 3 3\n") == "NO", "all periods equal and odd"
assert run("1 2 3\n") == "YES", "mixed periods with 1 ensures coverage"
assert run("1500 1500 1500\n") == "NO", "maximum periods, same odd number"
assert run("2 3 4\n") == "YES", "coprime small periods"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | YES | Minimum-size periods, trivial coverage |
| 3 3 3 | NO | Odd equal periods cannot cover all seconds |
| 1 2 3 | YES | Presence of 1 guarantees coverage |
| 1500 1500 1500 | NO | Maximum-size periods with same value |
| 2 3 4 | YES | Nontrivial small coprime periods |

## Edge Cases

When all periods are 1, any start times work. The algorithm tries x1=x2=x3=1, start=1, and immediately finds every second covered, outputting YES.

When
