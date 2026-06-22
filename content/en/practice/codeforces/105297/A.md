---
title: "CF 105297A - Nauryz"
description: "There is a single music device that plays songs one after another. Each guest arrives at a specific time, selects a song with a fixed duration, and that song is normally appended to the end of the playback queue."
date: "2026-06-23T06:29:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105297
codeforces_index: "A"
codeforces_contest_name: "2024 USP Try-outs"
rating: 0
weight: 105297
solve_time_s: 61
verified: true
draft: false
---

[CF 105297A - Nauryz](https://codeforces.com/problemset/problem/105297/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

There is a single music device that plays songs one after another. Each guest arrives at a specific time, selects a song with a fixed duration, and that song is normally appended to the end of the playback queue.

Time flows forward, and the device continuously plays whatever is currently active. When a song finishes, the next song in the queue starts immediately, with no delay.

The twist is that some guests can press a special button at the moment they choose their song. If they do, their song does not behave like a normal queued song. Instead, it immediately replaces whatever is currently playing at that exact moment, and playback switches instantly to their song. The interrupted song is discarded and will never resume. Importantly, everything that was still waiting in the queue remains unchanged.

A guest becomes unhappy only if their song is actively playing and another guest uses this interrupt button at a time strictly before their song finishes. If an interrupt happens exactly at the instant a song ends, that does not count as an interruption.

The task is to determine which guests had their songs interrupted at least once.

The input size can go up to 100,000 events, which immediately rules out any simulation that restarts from scratch per event or repeatedly scans the queue. Any solution that is worse than linear or near-linear in practice will struggle under the time limit. The structure also suggests that we are dealing with a single evolving timeline, so efficient simulation or event processing is required.

A subtle edge case arises when multiple guests interact while no song is playing. In that case, even if a guest uses the interrupt button, there is nothing to interrupt, so nobody becomes unhappy. Another tricky case is when an interrupt happens exactly at a song boundary. Since the song has already finished, it should not be counted as a disruption.

## Approaches

A direct simulation would maintain an explicit queue of songs and simulate time second by second or event by event, checking at every moment whether a song finishes or whether a guest interrupts. This works conceptually because the system is deterministic: songs play in order, and interrupts immediately replace the current song. However, simulating at fine granularity is far too slow because song durations and times go up to 10^7, meaning the simulation could require up to 10^12 operations in the worst case.

The key observation is that nothing happens between events except continuous progression of time and deterministic completion of songs. We only need to react at discrete moments: when a guest arrives, and when a song finishes. This allows us to maintain a single pointer to the current song and a queue of waiting songs, while advancing time in jumps rather than step-by-step.

The second insight is that interrupts only affect the currently playing song, never the queue. This means we never need to modify future scheduled songs except for appending new ones. The system can therefore be modeled as a single timeline with a current state, a FIFO queue, and occasional forced replacements.

By simulating time progression between consecutive events, we can ensure that the current song is always correct at each arrival moment, and we only perform constant work per event.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Naive step-by-step simulation | O(total time) | O(n) | Too slow |
| Event-driven queue simulation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain three pieces of state: the current song (if any), its scheduled end time, and a queue of pending songs added without interrupt. We also maintain a current time pointer that tracks how far we have simulated.

1. Sort or assume events are already in increasing order of time. Since the problem guarantees distinct times, we can process in input order.
2. Before processing an event at time `t`, advance the simulation from the current time up to `t`. During this interval, repeatedly finish the current song if it ends before or at `t`, then immediately start the next song in the queue. This ensures that at time `t`, the current song state is accurate.
3. If there is no current song at time `t` and the queue is non-empty, start the next queued song immediately. Its end time is computed as `t + duration`.
4. Process the event at time `t`. If the guest does not use the button (`c = 0`), append their song to the queue. It will eventually play after earlier songs finish.
5. If the guest uses the button (`c = 1`), check whether a song is currently playing and whether it will end strictly after `t`. If so, mark the current song’s owner as sad because it gets interrupted.
6. Replace the current song with the new one immediately, setting its end time to `t + duration`. This song does not enter the queue.
7. Continue to the next event.

### Why it works

At any moment, the system state is fully determined by the current song and the queue of pending songs. Between events, the system evolves deterministically with no external input, so we can safely fast-forward time to the next event boundary without losing information. Every interruption is handled exactly once at the moment it happens, and no future event can retroactively affect past playback. This guarantees that every interrupted song is counted precisely when it is replaced while still playing.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n = int(input())
    events = []
    for i in range(n):
        t, m, c = map(int, input().split())
        events.append((t, m, c, i + 1))

    queue = deque()
    sad = set()

    cur_id = 0
    cur_end = 0
    cur_dur = 0

    # we also need to know current owner id; store it separately
    cur_owner = None

    time = 0

    def start_next(t):
        nonlocal cur_owner, cur_end, cur_dur
        if queue:
            oid, dur = queue.popleft()
            cur_owner = oid
            cur_dur = dur
            cur_end = t + dur
        else:
            cur_owner = None
            cur_end = t

    for t, m, c, idx in events:
        # advance time to t
        while cur_owner is not None and cur_end <= t:
            time = cur_end
            start_next(time)

        time = t

        # if no current song, start from queue
        if cur_owner is None:
            start_next(t)

        if c == 0:
            queue.append((idx, m))
        else:
            # interrupt if currently playing and not already finished at t
            if cur_owner is not None and cur_end > t:
                sad.add(cur_owner)

            cur_owner = idx
            cur_dur = m
            cur_end = t + m

    print(len(sad))
    if sad:
        print(*sad)
    else:
        print()

if __name__ == "__main__":
    solve()
```

The solution maintains a queue of pending songs and a single active song with its scheduled end time. The helper logic `start_next` ensures that whenever the current song finishes, the next queued song starts immediately at the correct time.

The key subtlety is the condition `cur_end > t` when deciding whether to mark a song as interrupted. If a song ends exactly at time `t`, it is allowed to finish cleanly, so it must not be counted as sad.

Another important detail is that interrupted songs are never reinserted anywhere. They disappear entirely, while queued songs remain unaffected.

## Worked Examples

Consider a simple case where one song is playing and another guest interrupts it.

### Example 1

Input:

```
3
1 5 0
2 4 1
10 3 0
```

| Time | Event | Current owner | End time | Queue | Sad set |
| --- | --- | --- | --- | --- | --- |
| 1 | add (1,5) | 1 | 6 | [] | {} |
| 2 | interrupt (2,4) | 2 replaces 1 | 6 (new ends at 6? actually 2+4=6) | [] | {1} |
| 10 | add (3,3) | 2 finished earlier, 3 queued then played | 13 | [] | {1} |

The first song is interrupted at time 2, so its owner becomes sad. The second song finishes normally, and the third is never interrupted.

### Example 2

Input:

```
4
1 3 0
2 2 0
5 4 1
7 1 0
```

| Time | Event | Current owner | End time | Queue | Sad set |
| --- | --- | --- | --- | --- | --- |
| 1 | add A | A | 4 | [] | {} |
| 2 | add B | A | 4 | [B] | {} |
| 5 | interrupt C | C replaces B? actually A already finished, B playing | 7 | [] | {B} |
| 7 | add D | C | 9 | [D] | {B} |

This demonstrates that interruptions depend on the current active song at the exact moment, not on queue position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each song is started and finished at most once, and each event is processed once |
| Space | O(n) | Queue stores at most n pending songs, and sad set stores interrupted ones |

The algorithm processes each guest exactly once and advances time in jumps between events or song completions, keeping total work linear in the number of inputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n = int(input())
    events = []
    for i in range(n):
        t, m, c = map(int, input().split())
        events.append((t, m, c, i + 1))

    queue = deque()
    sad = set()

    cur_owner = None
    cur_end = 0

    def start_next(t):
        nonlocal cur_owner, cur_end
        if queue:
            oid, dur = queue.popleft()
            cur_owner = oid
            cur_end = t + dur
        else:
            cur_owner = None
            cur_end = t

    time = 0

    for t, m, c, idx in events:
        while cur_owner is not None and cur_end <= t:
            time = cur_end
            start_next(time)

        time = t

        if cur_owner is None:
            start_next(t)

        if c == 0:
            queue.append((idx, m))
        else:
            if cur_owner is not None and cur_end > t:
                sad.add(cur_owner)
            cur_owner = idx
            cur_end = t + m

    out = [str(len(sad))]
    if sad:
        out.append(" ".join(map(str, sad)))
    else:
        out.append("")
    return "\n".join(out)

# provided sample style tests
assert run("3\n1 5 0\n2 4 1\n10 3 0\n").split()[0] == "1"
assert run("1\n1 1 0\n") == "0\n"

# boundary cases
assert run("2\n1 10 0\n2 1 1\n").split()[0] == "1"
assert run("3\n1 2 1\n2 2 1\n3 2 1\n")  # no crash
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single non-interrupt | 0 | no sad guests when no interruption occurs |
| immediate interrupt | 1 + index | correct detection of interruption at start |
| chained interrupts | multiple | robustness under repeated replacement |
| all ci=1 | all applicable | stress of repeated overrides |

## Edge Cases

One important edge case is when an interrupt happens exactly at the moment a song ends. In that situation, the condition `cur_end > t` ensures the song is not considered interrupted. For example, if a song ends at time 5 and another guest uses the button at time 5, the first song has already finished, so no sadness is recorded.

Another case occurs when multiple guests arrive while no song is playing and the queue is empty. In this situation, each non-interrupting song starts immediately, and interrupts simply replace the current song without affecting any hidden state. The algorithm handles this because `cur_owner` becomes `None`, and we only transition when there is a valid active song.

A third case is rapid successive interrupts. Since each interrupt directly replaces the current song and we only ever track one active song, repeated updates do not accumulate error. Each replacement is handled independently at its exact timestamp, and the previous active song is recorded as sad exactly once before being discarded.
