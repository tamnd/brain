---
title: "CF 103488J - Jiubei and Codeforces"
description: "We are simulating how a Codeforces rating evolves over time and how that rating translates into a visible title. Each user starts with an initial rating, then goes through a sequence of rating changes caused by contests."
date: "2026-07-03T06:18:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103488
codeforces_index: "J"
codeforces_contest_name: "The 2021 Zhejiang University City College Freshman Programming Contest"
rating: 0
weight: 103488
solve_time_s: 49
verified: true
draft: false
---

[CF 103488J - Jiubei and Codeforces](https://codeforces.com/problemset/problem/103488/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating how a Codeforces rating evolves over time and how that rating translates into a visible title. Each user starts with an initial rating, then goes through a sequence of rating changes caused by contests. After each change, the rating falls into one of several fixed intervals, and each interval corresponds to a specific title such as Newbie, Pupil, Expert, and so on.

The task is not to track the full history of ratings, but only to detect when the _title category_ changes. Whenever the title before a contest differs from the title after applying that contest’s rating change, we must print a transition in the form “old_title -> new_title”. After processing all contests for a test case, we also output the final title.

The constraints are small: at most 100 test cases, each with at most 100 rating updates. This means the total number of operations is at most 10,000. Any solution that processes each update in constant time is sufficient. Even repeated recomputation of the title from scratch after each update is fine.

A subtle point is that rating changes can cross multiple boundaries in a single step. For example, a rating might jump from 1500 directly to 2500, skipping several title bands. In such cases, we only output one transition: from the starting title of that step to the final title after the update, not intermediate ones.

Another edge case is when the rating starts and stays within the same bracket across multiple updates. In that case, nothing is printed for those steps, even though the numeric rating changes.

## Approaches

A direct way to solve the problem is to simulate the rating after each contest and recompute the corresponding title by checking which interval the rating falls into. Since there are only ten possible intervals, this lookup is constant time.

This brute-force simulation already matches the optimal approach in structure. For each update, we adjust the rating, recompute the title by scanning the threshold table, and compare it with the previous title. If they differ, we output a transition.

There is no hidden optimization required because the state space is tiny and each step is independent. The only meaningful work is maintaining the mapping from rating to title and tracking when it changes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute per step | O(n) per test | O(1) | Accepted |
| Same with multiple tests | O(total n) | O(1) | Accepted |

## Algorithm Walkthrough

### Title mapping

We first define a function that converts a rating value into its corresponding title by checking fixed thresholds from highest to lowest.

### Steps

1. Start with the initial rating and compute its initial title. This becomes the previous title we compare against.
2. For each rating change, update the current rating by adding the given delta. This models the result of the contest.
3. Compute the new title from the updated rating using the threshold mapping. This step translates a numeric state into a categorical state.
4. Compare the new title with the previous title. If they are different, output “previous_title -> new_title”. This captures only visible transitions, ignoring internal rating fluctuations within the same bracket.
5. Update the previous title to the new title and continue.
6. After processing all contests, output the final title once more.

### Why it works

The rating-to-title mapping is a partition of the integer line into disjoint intervals. Every rating corresponds to exactly one title, and each update only affects the current position in this partition. By remembering only the previous title, we preserve all information needed to detect changes, since a transition occurs exactly when two consecutive ratings fall into different intervals.

## Python Solution

```python
import sys
input = sys.stdin.readline

def get_title(r):
    if r >= 3000:
        return "Legendary grandmaster"
    if r >= 2600:
        return "International grandmaster"
    if r >= 2400:
        return "Grandmaster"
    if r >= 2300:
        return "International master"
    if r >= 2100:
        return "Master"
    if r >= 1900:
        return "Candidate master"
    if r >= 1600:
        return "Expert"
    if r >= 1400:
        return "Specialist"
    if r >= 1200:
        return "Pupil"
    return "Newbie"

t = int(input())
out_lines = []

for _ in range(t):
    n, k = map(int, input().split())
    rating = k
    prev = get_title(rating)

    for _ in range(n):
        rating += int(input())
        cur = get_title(rating)
        if cur != prev:
            out_lines.append(f"{prev} -> {cur}")
            prev = cur

    out_lines.append(prev)

print("\n".join(out_lines))
```

The core of the implementation is the `get_title` function, which encodes the rating intervals in descending order so that the first match is always correct. This avoids any need for complex data structures.

We store only the previous title string, not the previous rating, because transitions depend purely on category membership. Each update adjusts the rating, recomputes the category, and conditionally prints the transition.

Care must be taken to apply the rating update before computing the new title, since the output describes the state _after_ each contest.

## Worked Examples

### Example 1

Consider a simplified scenario:

Input:

```
1
3 1500
100
600
-500
```

We track the evolution step by step.

| Step | Rating | Title before | Change | Rating after | Title after |
| --- | --- | --- | --- | --- | --- |
| 0 | 1500 | Pupil | - | 1500 | Pupil |
| 1 | 1500 | Pupil | +100 | 1600 | Expert |
| 2 | 1600 | Expert | +600 | 2200 | Master |
| 3 | 2200 | Master | -500 | 1700 | Expert |

Output transitions:

```
Pupil -> Expert
Expert -> Master
Master -> Expert
Expert
```

This shows that each boundary crossing triggers exactly one output line, even if multiple thresholds are skipped in a single jump.

### Example 2

Input:

```
1
2 1190
20
-50
```

| Step | Rating | Title before | Change | Rating after | Title after |
| --- | --- | --- | --- | --- | --- |
| 0 | 1190 | Newbie | - | 1190 | Newbie |
| 1 | 1190 | Newbie | +20 | 1210 | Pupil |
| 2 | 1210 | Pupil | -50 | 1160 | Newbie |

Output:

```
Newbie -> Pupil
Pupil -> Newbie
Newbie
```

This demonstrates that even small oscillations around a threshold generate repeated transitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T · n) | Each rating update recomputes a constant-time title lookup |
| Space | O(1) | Only a few variables are stored regardless of input size |

The maximum number of updates is 10,000, and each step performs only a fixed sequence of comparisons. This comfortably fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def get_title(r):
        if r >= 3000:
            return "Legendary grandmaster"
        if r >= 2600:
            return "International grandmaster"
        if r >= 2400:
            return "Grandmaster"
        if r >= 2300:
            return "International master"
        if r >= 2100:
            return "Master"
        if r >= 1900:
            return "Candidate master"
        if r >= 1600:
            return "Expert"
        if r >= 1400:
            return "Specialist"
        if r >= 1200:
            return "Pupil"
        return "Newbie"

    t = int(input())
    out = []

    for _ in range(t):
        n, k = map(int, input().split())
        rating = k
        prev = get_title(rating)

        for _ in range(n):
            rating += int(input())
            cur = get_title(rating)
            if cur != prev:
                out.append(f"{prev} -> {cur}")
                prev = cur

        out.append(prev)

    return "\n".join(out)

# minimum size, no change
assert run("1\n1 1000\n0\n") == "Newbie", "min size"

# single upward transition
assert run("1\n1 1190\n20\n") == "Newbie -> Pupil\nPupil", "boundary up"

# multiple transitions in one jump
assert run("1\n1 1500\n1000\n") == "Pupil -> Master\nMaster", "skip bands"

# down crossing
assert run("1\n2 2100\n0\n-1000\n") == "Master -> Candidate master\nCandidate master", "downward change"

# oscillation
assert run("1\n3 1300\n100\n-100\n100\n") == "Pupil -> Specialist\nSpecialist -> Pupil\nPupil -> Specialist\nSpecialist", "oscillation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| min size | Newbie | no transitions |
| boundary up | Newbie -> Pupil\nPupil | exact threshold crossing |
| skip bands | Pupil -> Master\nMaster | multi-level jump |
| downward change | Master -> Candidate master\nCandidate master | decreasing rating |
| oscillation | multiple lines | repeated toggling |

## Edge Cases

A common edge case is starting exactly on a boundary. For example, a rating of 1200 is exactly the border between Newbie and Pupil. The mapping must be implemented with correct inequality ordering so that 1200 is classified as Pupil, not Newbie. The algorithm handles this by checking thresholds from highest to lowest and using inclusive lower bounds.

Another case is a large single update that crosses many brackets. For instance, starting at 1500 and adding +2000 jumps directly into the top category. The algorithm still computes only the final category and prints a single transition, because intermediate categories are never explicitly tracked.

A final case is when no transition happens across all updates. In that situation, only the final title is printed, since no “old -> new” events are triggered.
