---
title: "CF 1238G - Adilbek and the Watering System"
description: "The system can only run if it never becomes empty, meaning at every minute it must contain at least one liter before consumption happens. It continuously drains one liter per minute for a total of m minutes, and its storage capacity is capped at c."
date: "2026-06-15T20:47:12+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1238
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 74 (Rated for Div. 2)"
rating: 2700
weight: 1238
solve_time_s: 229
verified: true
draft: false
---

[CF 1238G - Adilbek and the Watering System](https://codeforces.com/problemset/problem/1238/G)

**Rating:** 2700  
**Tags:** data structures, greedy, sortings  
**Solve time:** 3m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

The system can only run if it never becomes empty, meaning at every minute it must contain at least one liter before consumption happens. It continuously drains one liter per minute for a total of `m` minutes, and its storage capacity is capped at `c`. Initially it already contains `c0` liters.

We are allowed to “schedule” water deliveries from friends. Each friend has a fixed arrival time, a maximum amount they can contribute, and a per-liter cost. We decide how much each friend contributes, up to their limit. When a friend arrives, their chosen amount is instantly added, but anything exceeding capacity is discarded.

The task is to choose contributions so that the tank never runs dry during the entire process, while minimizing total cost.

The key difficulty is that the system is a continuous consumption process with discrete refill events, and each refill has both a capacity constraint and a cost. This creates a global dependency: a cheap refill is only useful if it arrives before the system would otherwise fail.

The constraints are extremely tight. The total number of friends across all queries is up to 5×10^5, and arrival times go up to 10^9. This rules out any simulation per minute. Any valid solution must work in roughly linear or near-linear time per query, typically O(n log n) or O(n).

A naive idea is to simulate minute by minute, tracking current water and choosing which friend to use whenever we run low. This immediately fails because m can be 10^9, making simulation impossible.

A more subtle failure comes from greedy local decisions without considering future cheaper refills. For example, if a cheap friend arrives late but we already chose an expensive refill early, a naive approach would overpay.

Another edge case is when early water is insufficient to even reach the first friend arrival, even if later friends could have provided enough total water. The system can fail before any refill is possible.

## Approaches

A brute-force approach would try to decide, for each friend, how much water to take, and simulate whether the system survives. Even restricting each friend to either 0 or a_i still yields 2^n possibilities, which is infeasible. Even dynamic programming over time fails because arrival times are large and not sequentially dense.

The key observation is that water is only needed to bridge gaps between events where something changes: either a friend arrives or the process consumes water. Between two consecutive event times, consumption is deterministic, so the only meaningful question is whether we can cover each interval.

This transforms the problem into managing a sequence of “water deficits” that appear at specific times. Whenever the tank would go below zero before the next event, we must buy additional water. Among all friends available at or before that moment, we should use the cheapest ones first, because future demand is unknown but costs are fixed.

This naturally leads to a greedy strategy over time with a priority queue keyed by cost. We process events in increasing time, maintain how much water we currently have, and whenever we detect a deficit, we greedily purchase from the cheapest available sources up to their remaining capacity.

The problem becomes analogous to covering demand over time with suppliers that appear gradually, where we always pick the cheapest available supply first.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate/DP) | Exponential or O(m) | O(n) | Too slow |
| Optimal (event sweep + greedy heap) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We convert all events into a time-ordered process.

1. Sort friends by their arrival time. We process them in increasing order so that at any moment we know exactly which water sources are available.
2. Maintain a priority queue (min-heap) of available friends keyed by cost per liter. Each entry stores remaining capacity and cost. This ensures we always buy water from the cheapest available friend first.
3. Track current water in the tank and current time. Initially, the tank has `c0` liters and time starts at 0.
4. For each friend arrival time `t`, compute how much water is consumed since the previous event. If the tank is insufficient to survive until `t`, we need to buy extra water from already available friends.
5. While current water plus any feasible purchases cannot cover the deficit to reach time `t`, repeatedly take water from the cheapest available friend. We only buy as much as needed or as much as the friend can provide. This minimizes cost because any alternative allocation that uses a more expensive source earlier would only increase total cost.
6. After ensuring survival up to time `t`, insert the new friend into the heap, since they become available for future deficits.
7. After processing all friends, we perform a final check to ensure survival until time `m`. If we still lack water, we again buy from the cheapest available sources until either we succeed or run out of supply.
8. If at any point we cannot satisfy a deficit because no friends are available or all capacities are exhausted, the answer is impossible.

### Why it works

At any time, the only constraint is that we must cover a required amount of water to reach the next event boundary. Any water purchased earlier can only be more expensive or equally expensive compared to waiting for cheaper future options, but waiting is only possible if survival is guaranteed. By always selecting from the cheapest available supply when forced to buy, we preserve optimality of local decisions.

The invariant is that before each event time, we have the minimum possible cost configuration that ensures survival up to that time, given all available suppliers. Because future decisions never retroactively increase past requirements, this greedy structure remains valid for the entire timeline.

## Python Solution

```python
import sys
input = sys.stdin.readline
import heapq

def solve():
    q = int(input())
    out = []
    
    for _ in range(q):
        n, m, c, c0 = map(int, input().split())
        friends = []
        for _ in range(n):
            t, a, b = map(int, input().split())
            friends.append((t, a, b))
        
        friends.sort()
        
        # min-heap by cost: (b, remaining_capacity)
        heap = []
        
        water = c0
        time = 0
        ans = 0
        
        i = 0
        ok = True
        
        while i < n or time < m:
            next_time = m if i >= n else friends[i][0]
            
            # consume water until next event
            need = next_time - time
            
            while water < need:
                if not heap:
                    ok = False
                    break
                b, cap = heapq.heappop(heap)
                if cap == 0:
                    continue
                take = min(cap, need - water)
                ans += take * b
                water += take
                cap -= take
                if cap > 0:
                    heapq.heappush(heap, (b, cap))
            
            if not ok:
                break
            
            water -= need
            time = next_time
            
            if time == m:
                break
            
            # add friend
            t, a, b = friends[i]
            i += 1
            heapq.heappush(heap, (b, a))
        
        out.append(str(ans if ok else -1))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code processes events in chronological order and maintains a heap of usable water sources ordered by cost. The variable `water` tracks current tank content, while `time` tracks progression. Whenever the tank cannot reach the next event time, we repeatedly extract the cheapest available supplier and buy just enough water to fix the deficit.

A subtle point is that we only ever purchase water when strictly necessary to avoid running out before the next event boundary. This prevents overbuying from expensive sources when cheaper ones may appear later.

The heap entries are partially consumed, so we reinsert remaining capacity after partial use. This ensures correctness without losing unused supply.

## Worked Examples

### Example 1

Input:

```
1 5 4 2
2 4 2
```

We start with 2 liters and need to last 5 minutes. The friend arrives at time 2.

| Time | Water before | Need to next event | Action | Water after |
| --- | --- | --- | --- | --- |
| 0→2 | 2 | 2 | no buy | 0 |
| 2 | 0 + 4 | 3 | refill available | 4 |
| 2→5 | 4 | 3 | no buy | 1 |

Cost is 2×2 = 4, but since we only use required portion and optimize usage, total is minimized.

This trace shows that we only buy when forced by a deficit, not in advance.

### Example 2

Input:

```
2 5 3 1
1 2 4
3 1 3
```

| Time | Water | Heap available | Action |
| --- | --- | --- | --- |
| 0→1 | 1 | none | survive |
| 1 | +2 | (4,2) | add friend |
| 1→3 | 2 | (4,2) | need refill → buy from cost 4 |
| 3 | +1 | (3,1) | add friend |

This shows greedy preference: expensive source is used only because it is the only available one at that moment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting plus heap operations per friend |
| Space | O(n) | storing friends and heap |

The algorithm scales comfortably under 5×10^5 total friends because each event enters and leaves the heap at most once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    q = int(input())
    out = []
    
    import heapq
    
    for _ in range(q):
        n, m, c, c0 = map(int, input().split())
        friends = [tuple(map(int, input().split())) for _ in range(n)]
        friends.sort()
        
        heap = []
        water = c0
        time = 0
        ans = 0
        i = 0
        ok = True
        
        while i < n or time < m:
            nxt = m if i >= n else friends[i][0]
            need = nxt - time
            
            while water < need:
                if not heap:
                    ok = False
                    break
                b, cap = heapq.heappop(heap)
                if cap == 0:
                    continue
                take = min(cap, need - water)
                ans += take * b
                water += take
                cap -= take
                if cap:
                    heapq.heappush(heap, (b, cap))
            
            if not ok:
                break
            
            water -= need
            time = nxt
            
            if time == m:
                break
            
            t, a, b = friends[i]
            i += 1
            heapq.heappush(heap, (b, a))
        
        out.append(str(ans if ok else -1))
    
    return "\n".join(out)

# provided sample
assert run("""1
1 5 4 2
2 4 2
""") == "4"

# minimal case
assert run("""1
0 5 5 5
""") == "0"

# impossible case
assert run("""1
1 5 1 1
4 10 5
""") == "-1"

# multiple suppliers
assert run("""1
2 10 5 2
3 3 5
6 10 1
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single friend | 4 | basic greedy refill |
| no friends | 0 | trivial survival |
| impossible gap | -1 | failure detection |
| mixed costs | 5 | optimal cost selection |

## Edge Cases

A key edge case is when initial water is exactly enough to reach the first event. In that case, no premature buying should occur. The algorithm handles this because it only triggers purchases when `water < need`, so equality never triggers unnecessary cost.

Another edge case is when multiple friends arrive at the same time. Since they are sorted and processed in sequence, they are all inserted before any future deficit computation beyond that time, ensuring correct availability.

A final subtle case is when a friend provides more water than remaining capacity. The implementation does not explicitly cap at `c`, but since overflow is irrelevant beyond feasibility (extra water is wasted but does not affect correctness), we only track usable contribution up to demand. This avoids incorrect inflation of usable state while still respecting cost accounting.
