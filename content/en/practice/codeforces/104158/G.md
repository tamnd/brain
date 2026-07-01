---
title: "CF 104158G - Crappy Typing"
description: "We are given a queue of employees, each associated with a fixed typing duration. There are $N$ employees standing in order, and we can place $M$ computers in front of them. At time zero, the first $M$ employees each occupy one computer and start typing."
date: "2026-07-02T01:10:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104158
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 01-27-23 Div. 1 (Advanced)"
rating: 0
weight: 104158
solve_time_s: 69
verified: true
draft: false
---

[CF 104158G - Crappy Typing](https://codeforces.com/problemset/problem/104158/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a queue of employees, each associated with a fixed typing duration. There are $N$ employees standing in order, and we can place $M$ computers in front of them. At time zero, the first $M$ employees each occupy one computer and start typing. Whenever a computer becomes free, the next employee in line immediately takes that computer and starts their test. This continues until all employees have finished. The finishing time of the whole process is the moment the last employee completes their typing.

The task is to determine the smallest number of computers $M$ such that the entire queue finishes within a given deadline $D$.

The key aspect is that assignment is strictly FIFO: a computer does not choose the shortest remaining job, it always serves the next person in line. Each machine behaves independently and repeatedly processes a sequence of jobs.

The constraints $N \le 10^5$ and $t_i \le 10^4$ indicate that any solution simulating the full process per candidate $M$ must be efficient. A naive simulation that repeatedly advances time step-by-step or scans the queue in an inefficient manner would be too slow. Even simulating each employee completion event without a heap can degrade to $O(N^2)$ in worst cases, which is not viable.

A subtle edge case arises when $M = 1$. Then the completion time is simply the sum of all $t_i$, and any greedy scheduling intuition must match this boundary. Another edge case is when $M \ge N$, where every employee gets a dedicated computer and the answer becomes $\max(t_i)$. Any implementation that does not explicitly handle or naturally include these cases risks incorrect boundary behavior.

## Approaches

A direct approach is to test a fixed number of computers $M$ and simulate the entire process. We assign the first $M$ jobs, then repeatedly pick the machine that becomes free the earliest, assign it the next job, and update its availability. Using a priority queue, each job assignment costs $O(\log M)$, so simulating all $N$ jobs costs $O(N \log M)$. This is correct because it faithfully models the process, but it is only useful once per candidate $M$.

To solve the actual problem, we need to find the smallest $M$ that satisfies the deadline condition. The crucial observation is that if a configuration with $M$ machines finishes within time $D$, then any larger number of machines can only reduce waiting time. No job becomes slower when we add more parallel servers, so feasibility is monotonic in $M$.

This monotonic structure allows binary search on $M$. For a fixed $M$, we simulate the process using a min-heap of machine availability times. Each job is assigned to the earliest finishing machine, and we track the maximum completion time. Binary search reduces the number of simulations to $O(\log N)$, giving a total complexity of $O(N \log N \log N)$, which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation for each M | $O(N^2 \log N)$ | $O(N)$ | Too slow |
| Binary search + heap simulation | $O(N \log N \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We treat the problem as a decision problem: given $M$, can we finish within time $D$?

1. Fix a candidate $M$ and simulate the scheduling process using a min-heap of size $M$. Each heap element represents the time when a computer becomes free. Initially, all $M$ computers are free at time 0.
2. Iterate through employees in order. For each employee $i$, extract the smallest value from the heap, which represents the earliest available computer. This is the machine that will finish its current load first.
3. Assign employee $i$ to that computer by adding $t_i$ to its availability time and pushing it back into the heap. This maintains the invariant that the heap always contains the next free time of each machine.
4. After processing all employees, the final answer for this configuration is the maximum value among all heap elements, which represents the last completion time.
5. If this completion time is at most $D$, then $M$ is feasible.
6. Binary search over $M$ from 1 to $N$, using the feasibility check to guide the search toward smaller valid values.

Why it works is based on a monotonic load distribution property. Increasing $M$ can only reduce or maintain the load per machine because jobs that previously queued behind busy machines now get earlier execution opportunities. The heap simulation always assigns each job to the earliest available machine, which is the only locally optimal choice consistent with the FIFO constraint. Since every assignment depends only on availability times and not future decisions, the simulation fully determines the schedule for a given $M$, and feasibility is well-defined and monotone.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def can(M, t, D):
    # initialize M machines, all free at time 0
    heap = [0] * M
    heapq.heapify(heap)

    for x in t:
        cur = heapq.heappop(heap)
        cur += x
        heapq.heappush(heap, cur)
        if cur > D:
            # optional early exit
            pass

    return max(heap) <= D

def solve():
    N, D = map(int, input().split())
    t = list(map(int, input().split()))

    lo, hi = 1, N

    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid, t, D):
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The core simulation uses a min-heap where each value tracks when a machine becomes available. The greedy assignment is forced by the model: the next employee always takes the machine that becomes free the earliest.

The binary search narrows down the smallest feasible $M$. The check function computes the actual completion time; we compare it against $D$.

A subtle implementation detail is that we track the maximum heap value at the end rather than trying to maintain a running finish time carefully. This avoids mistakes in partial reasoning about intermediate states. Another detail is that we cannot rely on early stopping inside the loop without carefully maintaining correctness, so the clean version simply completes the simulation.

## Worked Examples

### Sample 1

Input:

```
6 151
56 94 95 33 62 28
```

We test candidate values of $M$. For illustration, consider $M = 3$.

| Step | Heap state before | Assigned $t_i$ | Popped | Heap state after |
| --- | --- | --- | --- | --- |
| 1 | [0,0,0] | 56 | 0 | [0,0,56] |
| 2 | [0,0,56] | 94 | 0 | [0,56,94] |
| 3 | [0,56,94] | 95 | 0 | [56,94,95] |
| 4 | [56,94,95] | 33 | 56 | [89,94,95] |
| 5 | [89,94,95] | 62 | 89 | [94,94,95] |
| 6 | [94,94,95] | 28 | 94 | [94,122,95] |

Final completion time is 122, which is within 151, so $M=3$ is feasible. Trying $M=2$ would overload machines more heavily and exceed the limit, so the answer is 3.

This trace shows how the heap always assigns the next job to the earliest available machine and how backlog accumulates when $M$ is small.

### Sample 2

Input:

```
9 83
10 47 53 9 83 33 15 24 28
```

Testing $M = 5$:

| Step | Heap state before | Assigned $t_i$ | Popped | Heap state after |
| --- | --- | --- | --- | --- |
| 1 | [0,0,0,0,0] | 10 | 0 | [0,0,0,0,10] |
| 2 | [0,0,0,0,10] | 47 | 0 | [0,0,0,10,47] |
| 3 | [0,0,0,10,47] | 53 | 0 | [0,0,10,47,53] |
| 4 | [0,0,10,47,53] | 9 | 0 | [0,9,10,47,53] |
| 5 | [0,9,10,47,53] | 83 | 0 | [9,10,47,53,83] |
| 6 | [9,10,47,53,83] | 33 | 9 | [10,33,47,53,83] |
| 7 | [10,33,47,53,83] | 15 | 10 | [15,33,47,53,83] |
| 8 | [15,33,47,53,83] | 24 | 15 | [24,33,47,53,83] |
| 9 | [24,33,47,53,83] | 28 | 24 | [28,33,47,53,83] |

Final time is 83, matching the deadline, so 5 is feasible. Any smaller number would delay the large 83-task further, breaking the constraint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N \log N)$ | $O(N \log M)$ simulation inside binary search |
| Space | $O(N)$ | heap of size $M \le N$ |

The solution comfortably fits because $N = 10^5$, so even a few million heap operations remain within limits. Binary search reduces the number of full simulations to about 17, and each simulation is linearithmic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import heapq

    def can(M, t, D):
        heap = [0] * M
        heapq.heapify(heap)
        for x in t:
            cur = heapq.heappop(heap)
            cur += x
            heapq.heappush(heap, cur)
        return max(heap) <= D

    def solve():
        N, D = map(int, input().split())
        t = list(map(int, input().split()))
        lo, hi = 1, N
        while lo < hi:
            mid = (lo + hi) // 2
            if can(mid, t, D):
                hi = mid
            else:
                lo = mid + 1
        print(lo)

    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("6 151\n56 94 95 33 62 28\n") == "3"
assert run("9 83\n10 47 53 9 83 33 15 24 28\n") == "5"

# custom cases
assert run("1 10\n7\n") == "1", "single employee"
assert run("5 100\n1 1 1 1 1\n") == "1", "all equal small times"
assert run("5 3\n1 1 1 1 1\n") == "2", "tight deadline forces split"
assert run("4 10\n10 1 1 1\n") == "2", "heavy first job dominates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single job | 1 | base case |
| uniform tiny tasks | 1 | minimum machine suffices |
| tight deadline | 2 | correctness under constraint |
| heavy first job | 2 | load imbalance handling |

## Edge Cases

For $N = 1$, the heap has a single machine and the algorithm immediately returns 1, since the only completion time is $t_1$, matching the requirement.

When all $t_i$ are equal and small, the heap distributes tasks evenly across machines. For example, with $N = 4$, $t = [2,2,2,2]$, and large $D$, the simulation shows that one machine is enough if $D \ge 8$, but binary search correctly finds the smallest valid $M$ without overestimating.

When one task is much larger than others, such as $t = [100,1,1,1]$, the heap ensures the long task occupies a machine early, while short tasks fill others. With small $M$, the long task becomes the bottleneck, and feasibility fails unless enough machines exist.
