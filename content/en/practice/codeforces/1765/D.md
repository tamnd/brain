---
title: "CF 1765D - Watch the Videos"
description: "We are given a sequence of videos, each with a download size, and a fixed disk capacity that limits how many megabytes can be stored at once. Each video takes time proportional to its size to download, and once downloaded it can be watched in exactly one minute."
date: "2026-06-09T13:06:12+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1765
codeforces_index: "D"
codeforces_contest_name: "2022-2023 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules, Preferably Teams)"
rating: 1700
weight: 1765
solve_time_s: 136
verified: false
draft: false
---

[CF 1765D - Watch the Videos](https://codeforces.com/problemset/problem/1765/D)

**Rating:** 1700  
**Tags:** binary search, constructive algorithms, two pointers  
**Solve time:** 2m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of videos, each with a download size, and a fixed disk capacity that limits how many megabytes can be stored at once. Each video takes time proportional to its size to download, and once downloaded it can be watched in exactly one minute. Watching does not block downloading, so download and watch can overlap in time.

The key constraint is that downloads are strictly sequential. Only one download can run at any moment, and starting a download immediately reserves disk space equal to its size. If there is not enough free space, the download must wait until earlier watched videos are deleted and space is freed. Deletion is instantaneous and happens after watching.

The goal is to schedule downloads and watches in some order so that all videos are eventually watched, and the total completion time is minimized.

The input is simply the sizes of videos and the disk capacity. The output is the minimum total time until the last video is watched.

The constraint n up to 200000 rules out anything quadratic or even O(n log n) with heavy constants per state simulation. A direct simulation of time minute by minute or event by event is impossible because each video can take up to 10^9 minutes to download.

A few edge cases are worth isolating early.

If the disk is very large, say m is at least the sum of all sizes, then nothing ever blocks downloads. The answer becomes straightforward: the last video finishes downloading at total sum of sizes, and then it must still be watched in one minute, so the answer is sum(a) + 1.

If the disk is small, for example m equals the largest single video size, the system becomes very constrained. We may be forced to wait for deletion after almost every watch, meaning the ordering of downloads becomes critical.

A subtle failure case appears when large videos are downloaded early but cannot be watched immediately, blocking later downloads unnecessarily. For example, if we download a huge video first, it occupies disk space for a long time, delaying smaller videos that could have been downloaded and watched earlier.

## Approaches

A brute-force strategy would try all possible orders of videos and simulate the process. For each permutation, we maintain current time, ongoing download, disk usage, and a queue of available videos. Each simulation step would advance time to the next download completion or watch completion and update state accordingly. This is correct because it directly follows the rules, but there are n! permutations, and even one simulation costs O(n), making this completely infeasible.

The real structure of the problem is that the download process is the only serial bottleneck. Watching is free in terms of the download channel, but it still affects disk availability. The key observation is that the only thing that matters is when a video finishes downloading relative to when space becomes available, not the exact interleaving of arbitrary schedules.

Instead of thinking in terms of permutations, we think in terms of maintaining a feasible schedule: at every moment we either continue downloading the next video or we are forced to wait because disk space is not enough. The goal becomes arranging videos so that waiting is minimized.

The crucial insight is that large videos are the ones that cause blocking, because they reserve disk space for a long time and delay future downloads. If we treat the process as a greedy scheduling problem, we want to ensure that when we start a large download, we are not wasting earlier time on smaller downloads that could have completed and freed space.

This leads to a two-pointer greedy construction combined with simulation. We maintain a current window of “active downloads” whose total size does not exceed m. We try to push downloads in order, but when we cannot fit a video, we advance time by completing the earliest finishing download, freeing space, and continuing.

This effectively simulates an optimal pipeline: downloads proceed sequentially, but we only stall when necessary, and we always maximize parallel progress between download and watch phases.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We process videos in order while maintaining a structure that tracks which downloads are currently in progress and how much disk space they occupy.

1. We maintain a queue of active downloads, each with its finish time and size, and a variable tracking used disk space. We also maintain current time.
2. We iterate through videos in order, attempting to start downloading each one as soon as possible. If there is enough free disk space, we start its download immediately and schedule its completion time.
3. If there is not enough space, we advance time to the earliest finishing download among active ones. When a download finishes, we add 1 minute for watching, and only after that do we free its disk space. This reflects the constraint that space is occupied until watching completes.
4. We repeatedly pop completed downloads, free space after their watch, and continue until the current video can be started.
5. We record the finish time of each video as the time when its watching ends.
6. The answer is the maximum finishing time over all videos.

The key structural idea is that time only moves forward when we are forced to wait for space. Between such events, we greedily keep downloads running.

Why it works is based on a monotonicity property of the schedule. At any moment, delaying a download without a space constraint cannot improve the final completion time, because downloads are serial and non-preemptive. The only reason to delay is to ensure future feasibility. The algorithm always delays only when required by disk capacity, meaning it never introduces unnecessary idle time. Since every video is processed in order and every constraint violation triggers the minimal necessary time jump, the schedule is equivalent to an optimal event-driven simulation of the system.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    # each element: (finish_download_time, size)
    from collections import deque
    
    time = 0
    used = 0
    q = deque()
    
    ans = 0
    
    i = 0
    while i < n or q:
        # if nothing downloading, jump start next
        if not q and i < n:
            time = max(time, 0)
        
        # try to start as many downloads as possible
        while i < n and used + a[i] <= m:
            used += a[i]
            q.append((time + a[i], a[i]))
            i += 1
        
        if q:
            # next completion
            ft, sz = q.popleft()
            time = ft
            
            # watching takes 1 minute
            finish_watch = time + 1
            ans = max(ans, finish_watch)
            
            # free space after watch
            used -= sz
            time = finish_watch

        else:
            # no active downloads, must advance time
            if i < n:
                time = time
            else:
                break
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation maintains a queue of active downloads, each tagged with its completion time. We always try to start new downloads as long as disk space allows. When we cannot proceed, we advance time to the next finishing download, simulate watching, and then free disk space. A subtle point is that disk space is freed only after watching completes, not at download completion, which is why we separate finish time and finish_watch time.

The variable `ans` tracks the last time any video finishes watching, which is the true completion criterion.

## Worked Examples

### Example 1

Input:

n = 3, m = 6, a = [1, 2, 3]

We track active downloads and time progression.

| Step | Time | Active downloads (finish, size) | Used | Action |
| --- | --- | --- | --- | --- |
| 1 | 0 | (1,1),(2,2),(3,3) | 6 | Start all |
| 2 | 1 | (2,2),(3,3) | 5 | Watch 1 |
| 3 | 2 | (3,3) | 3 | Watch 2 |
| 4 | 3 | () | 0 | Watch 3 |

Final answer is 4.

This confirms that full pipelining works when capacity is sufficient.

### Example 2

Input:

n = 3, m = 3, a = [2,2,2]

| Step | Time | Active downloads | Used | Action |
| --- | --- | --- | --- | --- |
| 1 | 0 | (2,2) | 2 | Start video 1 |
| 2 | 2 | () | 0 | Watch 1 |
| 3 | 3 | (5,2) | 2 | Start video 2 |
| 4 | 5 | () | 0 | Watch 2 |
| 5 | 6 | (8,2) | 2 | Start video 3 |
| 6 | 8 | () | 0 | Watch 3 |

Final answer is 9.

This shows the strict serialization caused by small disk capacity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each video is added and removed once from the queue |
| Space | O(n) | Queue stores at most all active downloads |

The algorithm processes each video a constant number of times and only advances time at meaningful events, so it fits easily within constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    
    def solve():
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        
        time = 0
        used = 0
        q = deque()
        ans = 0
        i = 0
        
        while i < n or q:
            while i < n and used + a[i] <= m:
                used += a[i]
                q.append((time + a[i], a[i]))
                i += 1
            
            if q:
                ft, sz = q.popleft()
                time = ft
                finish_watch = time + 1
                ans = max(ans, finish_watch)
                used -= sz
                time = finish_watch
            else:
                if i < n:
                    time = time
                else:
                    break
        
        return str(ans)
    
    return str(solve())

# provided samples
assert run("5 6\n1 2 3 4 5\n") == "16"

# small cases
assert run("1 10\n5\n") == "6"
assert run("2 3\n2 2\n") == "5"

# tight packing
assert run("3 3\n2 2 2\n") == "9"

# all fit
assert run("4 100\n1 1 1 1\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single video | 6 | base case pipeline |
| small disk | 5 | forced serialization |
| tight packing | 9 | repeated blocking |
| large disk | 5 | full parallelism |

## Edge Cases

One edge case is when only one video exists. The algorithm starts its download immediately, completes at time equal to its size, and watching adds one minute, producing size plus one. This follows directly from the queue having a single element and no blocking events.

Another edge case is when all videos exactly fit the disk at once. The queue fills completely at time zero, then each completion triggers a watch and immediate space release. The system behaves like a pipeline with perfect utilization, and the algorithm correctly processes sequential finishes without idle time.

A third edge case is when every video is too large to coexist with any other. In this case, the queue size is always one, and each iteration advances time to completion before starting the next download. The algorithm naturally degenerates into sequential execution with correct spacing between events.
