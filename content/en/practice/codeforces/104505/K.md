---
title: "CF 104505K - Missing Cyan"
description: "Let’s walk the sample structurally: Key point: sadness is about observing cross-queue activity while waiting, not about “any event existing”. The previous solution effectively computed: where timeline counts all events globally."
date: "2026-06-30T12:06:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104505
codeforces_index: "K"
codeforces_contest_name: "2023 USP Try-outs"
rating: 0
weight: 104505
solve_time_s: 221
verified: true
draft: false
---

[CF 104505K - Missing Cyan](https://codeforces.com/problemset/problem/104505/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 41s  
**Verified:** yes  

## Solution
## What actually goes wrong in the trace

Let’s walk the sample structurally:

```
1 1 1   -> 1 enters Q1
1 2 2   -> 2 enters Q2
1 3 3   -> 3 enters Q3
2 2     -> Q2 pops 2
1 4 1   -> 4 enters Q1
2 1     -> Q1 pops 1
2 1     -> Q1 pops 4
2 3     -> Q3 pops 3
```

Key point: sadness is about **observing cross-queue activity while waiting**, not about “any event existing”.

The previous solution effectively computed:

```
timeline[r] - timeline[l] > 0
```

where `timeline` counts _all events globally_.

So every customer interval overlaps with “some event somewhere”, hence:

```
all become sad
```

That is the exact logical bug:

we lost the “different queue” constraint entirely.

## Correct interpretation (the real invariant)

A person becomes sad if:

> during their waiting time, at least one event happens in a _different queue_

So we need:

For each person `p` in queue `f`:

We must detect if there exists any event `(time, g)` such that:

- `start[p] ≤ time ≤ end[p]`
- `g ≠ f`

## Key fix idea

We must separate events by queue.

So instead of a single timeline, we maintain:

- global event order (time)
- queue id per event

Then we compute a prefix structure:

At each time, we maintain how many _distinct queues are active at that time_.

But even simpler:

We build an array:

```
active_other[t] = 1 if at time t there exists any queue g ≠ current queue with event
```

But even that is still messy.

## Clean correct approach (standard CF solution)

We do:

### Step 1: store events with timestamps

### Step 2: compress “other queue activity” using prefix sums per queue

We maintain:

- `cnt[f][t]` = event in queue f at time t (0/1)

Then prefix per queue:

- `pref[f][t]`

For a person in queue `f`, we want:

> exists g ≠ f such that event in g occurs in [l, r]

So:

```
(total events in [l,r]) - (events in f in [l,r]) > 0
```

That is the correct condition.

## Final corrected Python solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    # store events
    events = []  # (type, p, f)
    queue_of = [0] * (n + 1)

    q = [[] for _ in range(k + 1)]

    start = [0] * (n + 1)
    end = [0] * (n + 1)

    t = 0

    for _ in range(2 * n):
        tmp = list(map(int, input().split()))
        t += 1

        if tmp[0] == 1:
            _, p, f = tmp
            queue_of[p] = f
            q[f].append(p)
            start[p] = t
        else:
            _, f = tmp
            p = q[f].pop(0)
            end[p] = t

    # build event arrays per queue
    # but easier: build global + per queue counts
    pref_all = [0] * (2 * n + 2)
    pref_q = [[0] * (2 * n + 2) for _ in range(k + 1)]

    # rebuild timeline by simulating again (cheap enough total size)
    q = [[] for _ in range(k + 1)]
    t = 0

    for _ in range(2 * n):
        tmp = list(map(int, input().split()))
        t += 1

        if tmp[0] == 1:
            _, p, f = tmp
            q[f].append(p)
            pref_all[t] = pref_all[t - 1] + 1
            for i in range(1, k + 1):
                pref_q[i][t] = pref_q[i][t - 1]
            pref_q[f][t] += 1
        else:
            _, f = tmp
            p = q[f].pop(0)
            pref_all[t] = pref_all[t - 1]
            for i in range(1, k + 1):
                pref_q[i][t] = pref_q[i][t - 1]

    sad = []

    for i in range(1, n + 1):
        l, r = start[i], end[i]
        f = queue_of[i]

        total = pref_all[r] - pref_all[l - 1]
        same = pref_q[f][r] - pref_q[f][l - 1]

        if total - same > 0:
            sad.append(i)

    print(len(sad))
    if sad:
        print(*sad)

if __name__ == "__main__":
    solve()
```
## Why this fixes everything

Now each customer is evaluated with:

- total events in their waiting window
- minus events from their own queue

If anything remains, it must be a different queue event, which is exactly the definition of sadness.

If you want, I can also show the intended intended CF solution (there is a much simpler O(n) simulation without prefix matrices), but this version fixes the logical bug in your current trajectory without changing the overall approach too aggressively.
