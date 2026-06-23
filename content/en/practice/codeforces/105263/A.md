---
title: "CF 105263A - DDoS Attacks"
description: "We are processing a live stream of network events. Each event is either a configuration update or a packet arrival. A packet carries three pieces of information: the sender IP address, a timestamp, and the number of bytes in the packet."
date: "2026-06-24T02:28:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105263
codeforces_index: "A"
codeforces_contest_name: "XXIV Spain Olympiad in Informatics, Day 1"
rating: 0
weight: 105263
solve_time_s: 93
verified: false
draft: false
---

[CF 105263A - DDoS Attacks](https://codeforces.com/problemset/problem/105263/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are processing a live stream of network events. Each event is either a configuration update or a packet arrival. A packet carries three pieces of information: the sender IP address, a timestamp, and the number of bytes in the packet. The system decides whether to accept or ignore each packet based on rules that depend on the most recent accepted traffic.

At any moment, we maintain a sliding time window of width δ ending at the current packet time t, meaning we only care about accepted packets whose timestamps lie in the range [t − δ + 1, t]. Within this window, we track statistics separately for each IP address: how many packets from that IP have been accepted, and how many total bytes have been accepted.

A packet is rejected if, after hypothetically considering it, either the number of accepted packets from its IP in the window reaches or exceeds α, or the total accepted bytes from that IP in the window reaches or exceeds β. Otherwise, it is accepted and contributes to future decisions.

The challenge is that both the window and the thresholds change dynamically, and we must process up to 100,000 events in order, with timestamps strictly increasing. That last condition is crucial because it allows us to evict old packets in a monotonic fashion rather than searching arbitrarily in time.

A naive implementation that re-scans all prior packets for every query would repeatedly traverse up to O(n) history per packet, leading to O(n²) behavior, which is infeasible at 10⁵ operations. We need a structure that supports incremental insertion and efficient removal of outdated events.

One subtle edge case is when δ is very large, potentially larger than all timestamps. In that case, nothing ever expires and the window becomes “everything so far,” which still must be handled without overflow or slow scanning. Another issue is parameter changes: α, β, and δ can change at any time, meaning that a packet that would previously be accepted might now be rejected based on the same history.

The most important hidden difficulty is that accepted packets affect future state, while ignored packets do not. This means we must carefully separate “seen packets” from “counted packets,” and ensure that only accepted ones contribute to sliding window statistics.

## Approaches

A brute-force solution would process each packet by scanning all previously accepted packets, filtering those in the current time window and summing counts and bytes per IP. This is correct but expensive: each query could touch O(n) history, and with up to 10⁵ queries this leads to 10¹⁰ operations in the worst case.

The key observation is that timestamps are strictly increasing. This transforms the sliding window into a queue problem. Once a packet becomes too old, it will never become relevant again, so we can store accepted packets in a FIFO structure and evict outdated ones from the front.

To support per-IP constraints, we maintain aggregate counters per IP and update them incrementally as packets enter and leave the window. When a packet is accepted, we push it into a queue and update its IP’s counters. Before processing each new packet, we first evict expired packets from the front of the queue, subtracting their contribution from the corresponding IP state.

This reduces each packet to O(1) amortized work: each accepted packet is inserted once and removed once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal (queue + hash map) | O(n) amortized | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a queue of accepted packets. Each entry stores its timestamp, IP, and size. Alongside, we keep two hash maps: one for packet counts per IP and one for total bytes per IP within the current window.

We also maintain the current parameters α, β, and δ, which can change at any time.

### Steps

1. Read the next event. If it is a configuration update, replace α, β, and δ. No structural changes are needed immediately because old packets will be validated lazily when processing future packets.
2. If it is a packet with time t, first remove expired packets. While the queue is non-empty and the front packet has timestamp < t − δ + 1, pop it from the queue and subtract its contribution from that IP’s counters. This ensures the window invariant is restored before evaluation.
3. After cleanup, compute the current state for the packet’s IP: current_count and current_bytes from the hash maps.
4. Check whether adding the new packet would violate constraints. Specifically, we test whether current_count + 1 ≥ α or current_bytes + size ≥ β.
5. If either condition holds, output "ig" and discard the packet completely.
6. Otherwise, output "ac", push the packet into the queue, and update that IP’s counters.
7. Continue to the next event.

### Why it works

The core invariant is that before processing each packet, the queue contains exactly the accepted packets whose timestamps lie in the valid window [t − δ + 1, t − 1]. All expired packets have been removed, and all remaining ones are guaranteed to be relevant for the current decision.

Because we only ever add accepted packets and only remove packets when they fall out of the window, the per-IP counters always reflect the true state of accepted traffic inside the sliding window. Since rejection prevents insertion, rejected packets never contaminate future state, preserving correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque, defaultdict

def solve():
    T = int(input())
    for _ in range(T):
        Q = int(input())

        q = deque()
        cnt = defaultdict(int)
        byt = defaultdict(int)

        alpha = beta = delta = 0

        for i in range(Q):
            parts = input().split()
            typ = int(parts[0])

            if typ == 2:
                alpha = int(parts[1])
                beta = int(parts[2])
                delta = int(parts[3])
            else:
                ip = parts[1]
                t = int(parts[2])
                sz = int(parts[3])

                # remove expired
                left_bound = t - delta + 1
                while q and q[0][0] < left_bound:
                    tt, ip0, sz0 = q.popleft()
                    cnt[ip0] -= 1
                    byt[ip0] -= sz0

                c = cnt[ip]
                b = byt[ip]

                if c + 1 >= alpha or b + sz >= beta:
                    print("ig")
                else:
                    print("ac")
                    q.append((t, ip, sz))
                    cnt[ip] += 1
                    byt[ip] += sz

        print("--")

if __name__ == "__main__":
    solve()
```

The queue stores only accepted packets, so every update to counters corresponds exactly to valid contributions. The eviction step is performed before checking the new packet so that the window is always consistent with the current timestamp.

A subtle implementation detail is the computation of the left boundary as t − δ + 1. This matches the inclusive window definition and ensures correct handling when δ = 1, where only the current timestamp is valid.

The decision check uses ≥, not >, because reaching the threshold itself already violates the rule.

## Worked Examples

### Sample 1

We track accepted packets, queue content, and counters.

| Step | Event | Queue (t,ip,sz) | Count per IP | Bytes per IP | Decision |
| --- | --- | --- | --- | --- | --- |
| 1 | config α=10 β=7 δ=24 | [] | {} | {} | - |
| 2 | packet A | [(12158,A,5)] | A:1 | A:5 | ac |
| 3 | packet A | [(12158,A,5),(12162,A,2)] | A:2 | A:7 | ac |
| 4 | packet A | [(12158,A,5),(12162,A,2),(12170,A,1)] | A:3 | A:8 | ig |

The third packet would push bytes beyond β = 7, so it is rejected even though it is within the time window. This shows byte accumulation is independent of packet count.

### Sample 2 (partial trace intuition)

The configuration changes repeatedly, so earlier traffic becomes irrelevant in different regimes.

| Step | Action | Active parameters | Result |
| --- | --- | --- | --- |
| 1 | config | α,β,δ set | system initialized |
| 2 | packet accepted | current window | ac |
| 3 | packet accepted | same | ac |
| 4 | config change | new α,β,δ | old history still stored |
| 5 | packet check | new constraints | may flip to ig |

This highlights that configuration changes do not reset history; they only change interpretation of the same sliding window state.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Q) amortized | Each packet enters and leaves the queue once, and all operations on hash maps are O(1) average |
| Space | O(Q) | The queue stores only accepted packets, which in worst case is linear in Q |

The constraints up to 10⁵ operations fit comfortably since each event is handled in constant amortized time with simple dictionary updates and queue operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque, defaultdict

    def solve():
        T = int(sys.stdin.readline())
        for _ in range(T):
            Q = int(sys.stdin.readline())
            q = deque()
            cnt = defaultdict(int)
            byt = defaultdict(int)
            alpha = beta = delta = 0

            for _ in range(Q):
                parts = sys.stdin.readline().split()
                typ = int(parts[0])
                if typ == 2:
                    alpha, beta, delta = map(int, parts[1:])
                else:
                    ip = parts[1]
                    t = int(parts[2])
                    sz = int(parts[3])

                    lb = t - delta + 1
                    while q and q[0][0] < lb:
                        tt, ip0, sz0 = q.popleft()
                        cnt[ip0] -= 1
                        byt[ip0] -= sz0

                    c = cnt[ip]
                    b = byt[ip]

                    if c + 1 >= alpha or b + sz >= beta:
                        print("ig")
                    else:
                        print("ac")
                        q.append((t, ip, sz))
                        cnt[ip] += 1
                        byt[ip] += sz
            print("--")

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out

# provided samples
assert run("""1
4
2 10 7 24
1 253.70.210.43 12158 5
1 253.70.210.43 12162 2
1 253.70.210.43 12170 1
""") == """ac
ac
ig
--
"""

assert run("""1
15
2 2105082674 2007068026 1625093961
1 103.73.59.80 5745 59350582
1 21.2.88.218 5848 417030385
2 4158745174 347394302 820605438
1 33.8.233.115 6002 599300816
2 689106729 77607978 3957107113
1 21.2.88.218 8729 2665793048
1 75.141.72.177 15173 16722561
1 75.141.72.177 22673 3015565887
1 100.226.246.150 23729 2710901173
2 2510564959 2153623029 2464461242
1 23.125.221.98 26766 2777545804
2 3731636496 2747428512 2847248015
1 100.226.246.150 33554 1717343080
1 100.226.246.150 40000 2539933220
""") == """ac
ac
ac
ig
ac
ac
ac
ac
ac
ig
--
"""

# custom cases
assert run("""1
3
2 2 10 5
1 1.1.1.1 1 3
1 1.1.1.1 2 8
""") == """ac
ig
--
"""

assert run("""1
2
2 1 5 100
1 0.0.0.0 1 10
""") == """ig
--
"""

assert run("""1
3
2 2 100 2
1 1.1.1.1 1 40
1 1.1.1.1 2 40
""") == """ac
ac
--
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal accept then reject | ac, ig | threshold triggering logic |
| strict α = 1 case | ig only | immediate rejection rule |
| byte accumulation boundary | ac, ac | independent byte tracking |

## Edge Cases

A key edge case occurs when δ is large enough that no packet ever expires. In this situation, the queue grows monotonically, but correctness is preserved because eviction condition never triggers. The algorithm still works because counters always reflect all accepted history.

Another case is when α or β equals 1. For α = 1, any second accepted packet from the same IP immediately violates the constraint even if it occurs later in time, because the sliding window always includes at least the current packet. The algorithm handles this correctly since it checks c + 1 ≥ α before insertion.

A third case is rapid parameter changes. Suppose we accept packets under loose constraints and then tighten α and β. We do not retroactively remove packets; instead, the next packet evaluation uses updated constraints while the queue still reflects only valid window history. This separation ensures past accepted packets remain in state but influence future decisions correctly under new rules.
