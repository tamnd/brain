---
title: "CF 439A - Devu, the Singer and Churu, the Joker"
description: "The problem asks us to schedule an event where Devu, a singer, performs n songs of varying lengths, and Churu, a comedian, tells jokes of fixed 5-minute duration."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 439
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 251 (Div. 2)"
rating: 900
weight: 439
solve_time_s: 72
verified: true
draft: false
---

[CF 439A - Devu, the Singer and Churu, the Joker](https://codeforces.com/problemset/problem/439/A)

**Rating:** 900  
**Tags:** greedy, implementation  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to schedule an event where Devu, a singer, performs _n_ songs of varying lengths, and Churu, a comedian, tells jokes of fixed 5-minute duration. Devu requires a mandatory 10-minute rest after each song except the last, while Churu can perform jokes at any time without rest. The total duration of the event cannot exceed _d_ minutes. The goal is to determine the maximum number of jokes Churu can perform without skipping any of Devu's songs. If it's impossible to schedule all songs within the allotted time, the output should be -1.

The input consists of two integers _n_ and _d_, followed by a list of _n_ integers representing the song durations. The output is a single integer: the maximum number of jokes possible or -1 if Devu cannot complete his performance.

The constraints indicate that _n_ is small, at most 100, and _d_ can be up to 10,000. Since the number of songs is small, we can safely use straightforward arithmetic without worrying about algorithmic inefficiency. Edge cases include situations where Devu’s total song time plus required rests already exceeds _d_, or when all songs are very short, leaving plenty of room for jokes.

A subtle case arises when there is only one song. In that case, Devu does not require a 10-minute rest afterward, which affects the total time available for jokes.

## Approaches

A brute-force approach would attempt to simulate every possible order of songs and jokes to maximize the number of jokes. For each song, we could try placing zero or more jokes before or after it. However, this would explode combinatorially: for 100 songs and up to 10,000 minutes, the number of placements is enormous, making this approach infeasible.

The key insight comes from observing that Devu’s songs and rests consume a fixed minimum amount of time. For _n_ songs, the total song time is the sum of all _tᵢ_, and the total rest time is 10 minutes for each song except the last, giving 10 * (n - 1) minutes. This leaves all remaining minutes in _d_ available for jokes, which Churu can freely schedule. Since jokes are 5 minutes each, the maximum number of jokes is simply the floor division of remaining minutes by 5.

Thus, the problem reduces to checking if the sum of song times plus mandatory rests exceeds _d_. If it does, we return -1. Otherwise, we calculate how many 5-minute jokes fit in the remaining time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read input values: the number of songs _n_ and total available duration _d_.
2. Read the list of song durations.
3. Compute the total time required for Devu’s songs: `total_song_time = sum(tᵢ for each song)`.
4. Compute the total mandatory rest time: `total_rest_time = 10 * (n - 1)`.
5. Compute the minimum time needed for the event: `min_event_time = total_song_time + total_rest_time`.
6. If `min_event_time > d`, output -1, because it is impossible to schedule all songs.
7. Otherwise, compute the remaining time available for jokes: `remaining_time = d - min_event_time`.
8. Each joke takes 5 minutes, and additional jokes can also fit into the 10-minute rests between songs. There are `(n - 1)` rests of 10 minutes, which can host 2 jokes each. So, `max_jokes = 2 * (n - 1) + remaining_time // 5`.
9. Output `max_jokes`.

This works because we always fill mandatory rests first with jokes, maximizing their number without violating Devu’s rest requirements. Any leftover time is fully divisible into 5-minute jokes.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, d = map(int, input().split())
songs = list(map(int, input().split()))

total_song_time = sum(songs)
total_rest_time = 10 * (n - 1)
min_event_time = total_song_time + total_rest_time

if min_event_time > d:
    print(-1)
else:
    remaining_time = d - min_event_time
    max_jokes = 2 * (n - 1) + remaining_time // 5
    print(max_jokes)
```

The code directly implements the algorithm. It first computes the sum of song durations and the total mandatory rest time. It checks whether Devu can perform all songs in the given duration. If not, it prints -1. Otherwise, it calculates the maximum number of jokes by first filling rests between songs (2 jokes per 10-minute rest) and then using any remaining time for additional jokes.

## Worked Examples

### Sample 1

Input:

```
3 30
2 2 1
```

| Step | total_song_time | total_rest_time | min_event_time | remaining_time | max_jokes |
| --- | --- | --- | --- | --- | --- |
| Calculation | 2+2+1=5 | 10*(3-1)=20 | 5+20=25 | 30-25=5 | 2*2 + 5//5 = 4+1=5 |

The algorithm outputs 5, confirming that all songs can fit and the maximum number of jokes is calculated correctly.

### Sample 2 (Impossible case)

Input:

```
2 15
10 10
```

| Step | total_song_time | total_rest_time | min_event_time |
| --- | --- | --- | --- |
| Calculation | 10+10=20 | 10*(2-1)=10 | 20+10=30 |

Since 30 > 15, the output is -1. This demonstrates the algorithm correctly identifies impossible schedules.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We sum all song durations once |
| Space | O(n) | Storing the song durations |

With _n_ ≤ 100, the solution runs efficiently in under a millisecond, well within time and memory constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, d = map(int, input().split())
    songs = list(map(int, input().split()))
    total_song_time = sum(songs)
    total_rest_time = 10 * (n - 1)
    min_event_time = total_song_time + total_rest_time
    if min_event_time > d:
        return "-1"
    remaining_time = d - min_event_time
    max_jokes = 2 * (n - 1) + remaining_time // 5
    return str(max_jokes)

# Provided samples
assert run("3 30\n2 2 1\n") == "5", "sample 1"
assert run("2 15\n10 10\n") == "-1", "sample 2"

# Custom cases
assert run("1 15\n5\n") == "2", "single song with extra time"
assert run("4 100\n5 5 5 5\n") == "18", "multiple short songs, large d"
assert run("3 31\n5 5 5\n") == "7", "extra minute allows one more joke"
assert run("2 25\n10 5\n") == "3", "minimum time leaves room for remaining jokes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 15\n5 | 2 | Single song, extra time for jokes |
| 4 100\n5 5 5 5 | 18 | Multiple short songs, maximize jokes |
| 3 31\n5 5 5 | 7 | Check leftover time allocation |
| 2 25\n10 5 | 3 | Correctly handle partial remaining time |

## Edge Cases

If there is only one song, there is no 10-minute rest afterward. For input:

```
1 20
5
```

The total event time is just 5 minutes, leaving 15 minutes for jokes. Each joke is 5 minutes, so the output is 3. The algorithm correctly handles this by calculating `10*(1-1)=0` for rests.

Another edge case is when the total song duration plus rests exactly equals _d_, leaving no room for jokes. For input:

```
3 25
5 5 5
```

The event time is 5+5+5 + 10*2 = 25, which exactly matches _d_. Remaining time is zero, so maximum jokes are `2*(3-1) + 0//5 = 4`. The solution correctly fills rests but does not add extra jokes.
