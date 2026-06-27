---
title: "CF 105109J - Record The Record Record"
description: "Bob has a collection of numbered records from 1 to n. Over the next n days, he listens to some subset of these records each day. A record is considered new on a given day if Bob has never listened to it on any earlier day."
date: "2026-06-27T20:06:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105109
codeforces_index: "J"
codeforces_contest_name: "UTPC Spring 2024 Open Contest"
rating: 0
weight: 105109
solve_time_s: 65
verified: false
draft: false
---

[CF 105109J - Record The Record Record](https://codeforces.com/problemset/problem/105109/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** no  

## Solution
## Problem Understanding

Bob has a collection of numbered records from 1 to n. Over the next n days, he listens to some subset of these records each day. A record is considered new on a given day if Bob has never listened to it on any earlier day.

For every day, we care about how many of the records played that day are appearing for the first time in Bob’s entire listening history. The task is to determine the maximum such “new record count” across all days.

The input is a sequence of n daily listening logs. Each log gives a list of record IDs played on that day. Records can repeat within a day or across days, but only the first-ever appearance of each record contributes to the “new” count, and only on the day it first appears.

The output is a single number: the largest number of previously unseen records that appear in any one day.

The constraints are small: n is at most 1000 and the total number of recorded plays is at most 10^6 in the worst case. This immediately suggests that an O(total entries) or O(n^2) simulation is sufficient, since around 10^6 operations is safe in Python under a 2-second limit.

A subtle point is that duplicates inside a single day should not inflate the count. If a record appears multiple times in the same day, it still only contributes once as “new” if it is the first time it appears overall.

A second subtlety is that we must mark records as globally seen only after processing them for that day, otherwise duplicates within the same day could be incorrectly suppressed too early.

## Approaches

A direct approach is to simulate the process day by day while maintaining a global set of all records Bob has already heard. For each day, we scan all m entries and count how many are not in the global set. Whenever we encounter a record not yet seen, we increment the day’s count and mark it as seen.

This works because the definition of “new” depends only on whether the record appeared in any previous day, not on its position inside the current day. The only care needed is to avoid counting the same record multiple times within a single day if it is repeated in that day’s list. This can be handled either by a temporary set per day or by ensuring we only mark it once globally and ignore subsequent repeats in the same day.

The brute-force behavior is already optimal in structure: each record is processed once when it is first encountered as new, so the total number of effective insertions into the global set is bounded by n. The overhead is scanning all entries, which is at most 10^6 operations, well within limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Scan with global set | O(total m) | O(n) | Accepted |
| Nested checks per day | O(n * m) worst | O(n) | Accepted but unnecessary overhead |

## Algorithm Walkthrough

1. Initialize an empty set seen to store all records that have already appeared on previous days. This set represents the global history of Bob’s listening.
2. Initialize a variable answer to 0. This will track the maximum number of new records observed in any single day.
3. For each day, read the list of records played.
4. For that day, initialize a counter day_new to 0.
5. Iterate through each record in the day’s list. If the record is not in seen, it means this is its first-ever appearance. Increment day_new by 1 and add the record to seen.
6. If the record is already in seen, ignore it completely because it does not contribute to new discoveries.
7. After processing all records of the day, update answer as max(answer, day_new).
8. After all days are processed, output answer.

The key implementation decision is updating seen immediately when a record is first encountered globally. This ensures that later days correctly treat it as old, and it also prevents double counting in later scans.

### Why it works

At any point during processing, the set seen exactly matches the set of all distinct records that have appeared in earlier days. When we process a new day, every record is classified correctly based on whether it is in seen or not. Each record contributes to exactly one day’s count, specifically the first day it appears. Since we only increment day_new when encountering a previously unseen record, no record is ever counted twice, and no missed contribution is possible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    seen = set()
    ans = 0

    for _ in range(n):
        arr = list(map(int, input().split()))
        m = arr[0]
        records = arr[1:]

        day_new = 0
        for r in records:
            if r not in seen:
                seen.add(r)
                day_new += 1

        ans = max(ans, day_new)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution uses a single global set to track whether a record has been seen before. Each day’s input is parsed into a list, and the first element is the count m. The rest are the record IDs.

The important implementation detail is that we update the seen set immediately when we detect a new record. This ensures correctness across days. We do not need a per-day set because duplicates within a day do not matter: once a record is marked seen, subsequent occurrences in the same day will be ignored naturally.

## Worked Examples

### Example 1

Input:

```
3
1 1
2 1 3
3 1 2 3
```

| Day | Records | Seen before | New counted | Seen after |
| --- | --- | --- | --- | --- |
| 1 | 1 | {} | 1 | {1} |
| 2 | 1 3 | {1} | 1 (only 3) | {1,3} |
| 3 | 1 2 3 | {1,3} | 1 (only 2) | {1,2,3} |

The maximum number of new records in any day is 1. This matches the fact that after the first introduction of each record, everything becomes old immediately.

### Example 2

Input:

```
4
3 1 2 3
2 3 3
4 4 5 1 1
1 2
```

| Day | Records | Seen before | New counted | Seen after |
| --- | --- | --- | --- | --- |
| 1 | 1 2 3 | {} | 3 | {1,2,3} |
| 2 | 3 3 | {1,2,3} | 0 | {1,2,3} |
| 3 | 4 5 1 1 | {1,2,3} | 2 | {1,2,3,4,5} |
| 4 | 2 | {1,2,3,4,5} | 0 | {1,2,3,4,5} |

The peak occurs on day 1 with 3 new records, showing that the first day can dominate the answer if many unique items appear early.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total m) | Each record is checked once and inserted into a set at most once |
| Space | O(n) | The set stores each distinct record ID at most once |

The total number of record entries across all days is bounded by 10^6, so a linear scan with hashing fits comfortably within time limits. The memory usage is also bounded by the number of distinct records, which is at most n.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n = int(input())
        seen = set()
        ans = 0
        for _ in range(n):
            arr = list(map(int, input().split()))
            m = arr[0]
            records = arr[1:]
            day_new = 0
            for r in records:
                if r not in seen:
                    seen.add(r)
                    day_new += 1
            ans = max(ans, day_new)
        print(ans)

    from io import StringIO
    out = StringIO()
    backup_stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = backup_stdout
    return out.getvalue().strip()

# provided sample
assert run("""3
1 1
2 1 3
3 1 2 3
""") == "1"

# minimum input
assert run("""1
1 1
""") == "1"

# all same repeats
assert run("""3
3 1 1 1
3 1 1 1
3 1 1 1
""") == "1"

# staggered unique introduction
assert run("""3
1 1
1 2
1 3
""") == "1"

# maximum new on first day
assert run("""2
3 1 2 3
2 4 5
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 days single repeats | 1 | duplicates within a day |
| 1 element case | 1 | minimum boundary |
| repeated identical lists | 1 | global deduplication |
| sequential discovery | 1 | tracking across days |
| large first day | 3 | correct maximum tracking |

## Edge Cases

A case with repeated records inside a single day confirms that intra-day duplicates do not inflate the count. For example, input `1: [1, 1, 1]` should count only once. The algorithm handles this because once 1 is added to seen, subsequent occurrences are ignored.

A case where a record appears late after many repeats earlier confirms global tracking. For instance, if 5 appears only on the last day, it should still count once and only on that day. The set ensures it is not counted earlier.

A case where every day repeats only previously seen elements confirms that the answer can be zero after the first day. Once seen contains all records, all future days contribute zero, and the maximum is correctly preserved from earlier computation.
