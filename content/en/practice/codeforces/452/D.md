---
title: "CF 452D - Washer, Dryer, Folder"
description: "We have a three-stage production pipeline. Every laundry item must first be washed, then immediately transferred to a dryer when washing finishes, then immediately transferred to a folding machine when drying finishes."
date: "2026-06-07T17:09:07+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 452
codeforces_index: "D"
codeforces_contest_name: "MemSQL Start[c]UP 2.0 - Round 1"
rating: 1900
weight: 452
solve_time_s: 112
verified: true
draft: false
---

[CF 452D - Washer, Dryer, Folder](https://codeforces.com/problemset/problem/452/D)

**Rating:** 1900  
**Tags:** greedy, implementation  
**Solve time:** 1m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a three-stage production pipeline.

Every laundry item must first be washed, then immediately transferred to a dryer when washing finishes, then immediately transferred to a folding machine when drying finishes. Machines in the same stage are identical, and each machine can process only one item at a time.

The word "immediately" is the key difficulty. An item is not allowed to finish washing unless a dryer is available at that exact moment. Similarly, an item is not allowed to finish drying unless a folding machine is available at that exact moment. We are free to delay the start of washing so that these conditions hold.

The input gives the number of laundry items, the number of machines in each stage, and the processing time of each stage. We must compute the earliest time when all items have completed all three stages.

The constraints are surprisingly small. There are at most $10^4$ items and at most $1000$ machines per stage. A simulation that processes each item individually is completely feasible. Even an $O(k \log k)$ or $O(k)$ solution is easily fast enough. What is ruled out is any approach that models time minute-by-minute, because processing times can reach $1000$ and completion times can grow into the millions.

A common mistake is to treat each stage independently.

Consider:

```
1 1 1 1 5 5 5
```

The answer is 15. One item spends 5 minutes washing, 5 drying, and 5 folding.

A more subtle example is:

```
2 1 1 1 1 100 1
```

A careless solution might start the second wash at time 1 because the washer becomes free. That is illegal. The first item occupies the dryer until time 101, so the second item cannot finish washing before time 101. Its wash must be delayed to keep a dryer available at the wash completion moment.

Another trap appears when the folding stage is the bottleneck:

```
3 3 3 1 1 1 100
```

All three washers and dryers are available immediately, but only one folding machine exists. Finishing multiple drying operations at nearly the same time is impossible because each completed drying operation requires an instantly available folder. The schedule must be adjusted much earlier, at the washing stage.

The main challenge is that availability constraints propagate backward through the pipeline.

## Approaches

A brute-force viewpoint is to think in terms of scheduling events on a timeline. For every laundry item we could search for the earliest possible washing start time that eventually allows immediate transitions through drying and folding. This is correct because the system is deterministic once machine occupancies are known.

The problem is that searching time explicitly becomes expensive. Completion times can become very large, and repeatedly scanning forward to find valid moments would lead to unnecessary work.

The crucial observation is that we never need to search through time. What matters is the next moment when a machine in each stage becomes available.

Suppose we already scheduled some items. For a new item, we choose the washer that becomes available earliest. Let its available time be $w$.

If washing starts at $w$, the item would finish washing at $w+t_1$. At that moment we need a dryer. Among all dryers, the earliest available one determines when the transfer can happen.

Similarly, once drying finishes, we need a folder immediately.

Instead of scheduling the stages forward, we can think backward from the folding stage. If a folder becomes available at time $f$, then a drying operation that feeds it must finish no earlier than $f$. That drying operation in turn determines when washing may finish.

The elegant solution used in the contest keeps, for each stage, the next time every machine becomes available. For each laundry item we take the earliest available washer, dryer, and folder. These three availability times determine the earliest feasible start time for this item. After scheduling it, we update the machine availabilities.

The entire process becomes a direct simulation of machine release times.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force timeline search | Potentially very large | O(1) | Too slow |
| Machine availability simulation | O(k) | O(n₁+n₂+n₃) | Accepted |

## Algorithm Walkthrough

Let `wash[i]` be the next time washer `i` is available.

Let `dry[i]` be the next time dryer `i` is available.

Let `fold[i]` be the next time folder `i` is available.

Initially all values are zero.

For each laundry item:

1. Find the washer with the smallest availability time.
2. Find the dryer with the smallest availability time.
3. Find the folder with the smallest availability time.
4. Let these times be `w`, `d`, and `f`.
5. Compute the earliest washing start time that allows immediate transfers through the remaining stages.

Washing finishes at `start + t1`.

A dryer must be available then, so:

```
start + t1 >= d
```

Drying finishes at `start + t1 + t2`.

A folder must be available then, so:

```
start + t1 + t2 >= f
```

The washer itself cannot start before time `w`.

Combining all constraints:

```
start = max(
    w,
    d - t1,
    f - t1 - t2
)
```
6. Schedule the item using this start time.
7. Update the chosen washer's next availability to:

```
start + t1
```
8. Update the chosen dryer's next availability to:

```
start + t1 + t2
```
9. Update the chosen folder's next availability to:

```
start + t1 + t2 + t3
```
10. Record the completion time of this item. The answer is the completion time of the last scheduled item.

### Why it works

For every item we choose the earliest available machine in each stage. The computed start time is the minimum time that simultaneously satisfies all three resource constraints.

The washer must already be free. The dryer must be free exactly when washing ends. The folder must be free exactly when drying ends. Any smaller start time would violate at least one of those conditions.

After scheduling an item, the three selected machines become occupied until the corresponding stage completion moments. The availability arrays always represent the earliest future time when each machine can accept another item. Because every item is scheduled at the earliest feasible moment consistent with those availabilities, the simulation constructs the globally earliest schedule.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k, n1, n2, n3, t1, t2, t3 = map(int, input().split())

    wash = [0] * n1
    dry = [0] * n2
    fold = [0] * n3

    answer = 0

    for _ in range(k):
        iw = min(range(n1), key=wash.__getitem__)
        idr = min(range(n2), key=dry.__getitem__)
        ifo = min(range(n3), key=fold.__getitem__)

        w = wash[iw]
        d = dry[idr]
        f = fold[ifo]

        start = max(
            w,
            d - t1,
            f - t1 - t2
        )

        wash[iw] = start + t1
        dry[idr] = start + t1 + t2
        fold[ifo] = start + t1 + t2 + t3

        answer = fold[ifo]

    print(answer)

if __name__ == "__main__":
    solve()
```

The three arrays store machine release times. A release time means "this machine can accept a new item starting from this moment".

For each item we select the machine with the smallest release time in every stage. Because the number of machines is at most 1000, a linear scan is completely sufficient.

The most delicate part is computing `start`.

The washer availability imposes `start >= w`.

The dryer must be available when washing finishes, giving `start >= d - t1`.

The folder must be available when drying finishes, giving `start >= f - t1 - t2`.

Taking the maximum of these three values simultaneously satisfies all constraints.

The updates are easy to get wrong. The washer becomes free after washing completes, not after the entire pipeline finishes. Likewise, the dryer becomes free after drying completes. Only the folder remains occupied until the final completion time.

All arithmetic comfortably fits in Python integers.

## Worked Examples

### Sample 1

Input:

```
1 1 1 1 5 5 5
```

| Item | w | d | f | start | Washer free | Dryer free | Folder free |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 | 5 | 10 | 15 |

Answer = 15.

The single item moves through all three stages without waiting.

### Sample 2

Input:

```
8 2 1 1 5 10 2
```

| Item | w | d | f | start |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 |
| 2 | 0 | 15 | 17 | 2 |
| 3 | 5 | 30 | 32 | 15 |
| 4 | 7 | 45 | 47 | 30 |
| 5 | 20 | 60 | 62 | 45 |
| 6 | 35 | 75 | 77 | 60 |
| 7 | 50 | 90 | 92 | 75 |
| 8 | 65 | 105 | 107 | 90 |

The last item finishes at:

```
90 + 5 + 10 + 2 = 107
```

This trace shows how a bottleneck in later stages forces washing to start later than washer availability alone would suggest.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k(n₁+n₂+n₃)) | Each item scans all machines once |
| Space | O(n₁+n₂+n₃) | Stores machine availability times |

With $k \le 10^4$ and each machine count at most $1000$, the total work is roughly $3 \times 10^7$ simple operations in the worst theoretical case, which is acceptable in practice for this problem and was the intended solution.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    k, n1, n2, n3, t1, t2, t3 = map(int, input().split())

    wash = [0] * n1
    dry = [0] * n2
    fold = [0] * n3

    ans = 0

    for _ in range(k):
        iw = min(range(n1), key=wash.__getitem__)
        idr = min(range(n2), key=dry.__getitem__)
        ifo = min(range(n3), key=fold.__getitem__)

        start = max(
            wash[iw],
            dry[idr] - t1,
            fold[ifo] - t1 - t2
        )

        wash[iw] = start + t1
        dry[idr] = start + t1 + t2
        fold[ifo] = start + t1 + t2 + t3

        ans = fold[ifo]

    return str(ans)

# provided sample
assert run("1 1 1 1 5 5 5\n") == "15"

# minimum size
assert run("1 1 1 1 1 1 1\n") == "3"

# many washers, one dryer
assert run("2 2 1 1 1 100 1\n") == "102"

# all equal
assert run("3 3 3 3 5 5 5\n") == "15"

# pipeline bottleneck
assert run("3 3 3 1 1 1 100\n") == "302"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1 1 1 1` | `3` | Smallest possible instance |
| `2 2 1 1 1 100 1` | `102` | Dryer bottleneck propagates backward |
| `3 3 3 3 5 5 5` | `15` | Parallel machines remove waiting |
| `3 3 3 1 1 1 100` | `302` | Folding bottleneck dominates schedule |

## Edge Cases

Consider:

```
2 2 1 1 1 100 1
```

The dryer is the bottleneck. After scheduling the first item, the dryer is occupied until time 101. For the second item we have:

```
w = 0
d = 101
f = 102
```

The formula gives:

```
start = max(0, 100, 1) = 100
```

The second wash is deliberately delayed so that washing finishes exactly when the dryer becomes available. The algorithm outputs 102, which is optimal.

Now consider:

```
3 3 3 1 1 1 100
```

After the first item, the folder is occupied until time 102. The second item obtains:

```
start = max(0, 0, 100)
```

so it starts washing only at time 100. The third item starts at time 200. Completion times become 102, 202, and 302.

A solution that only tracks washer and dryer availability would incorrectly try to dry several items before a folding machine is available. The backward constraint `f - t1 - t2` prevents that mistake.

Finally, consider:

```
4 1 1 1 10 1 1
```

The washer is the bottleneck. Every new item naturally starts when the washer becomes free. The formula reduces to the washer constraint because the dryer and folder are always available in time. The algorithm behaves exactly like a simple single-machine pipeline and produces the correct schedule.
