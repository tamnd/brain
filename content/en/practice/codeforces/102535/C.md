---
title: "CF 102535C - Working with Locks 3"
description: "Perry owns a collection of numbered keys, and each key can unlock only the locks immediately next to its own number. The locks form a simple line from 1 to 1,000,000,000."
date: "2026-08-07T05:00:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102535
codeforces_index: "C"
codeforces_contest_name: "2020 UP ACM Algolympics Elimination Round"
rating: 0
weight: 102535
solve_time_s: 219
verified: true
draft: false
---

[CF 102535C - Working with Locks 3](https://codeforces.com/problemset/problem/102535/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

Perry owns a collection of numbered keys, and each key can unlock only the locks immediately next to its own number. The locks form a simple line from 1 to 1,000,000,000. For every lock that appears in the input list of active days, we need to determine whether at least one of its neighboring numbers exists in Perry's key collection. The answer is the number of active locks that can be opened.

The input gives the set of key positions first. The second important set is the collection of lock positions that will appear during the active days. We do not need to process all possible locks because there can be a billion of them, only the specific locks listed in the input matter.

Both the number of keys and the number of queried locks can reach 100,000. With a two second limit, a solution should stay close to linear time. Checking every key against every lock would require up to 10,000,000,000 comparisons, which is far beyond what is practical. A solution around O(k + L) or O((k + L) log k) is appropriate.

There are several edge cases where an implementation can easily fail.

A lock at position 1 only has one possible key, key 2. Treating it as if key 0 exists gives an incorrect answer. For example:

```
1
0
1
1
```

is not a valid input because key numbers start at 1, but the equivalent valid case is:

```
1
3
1
1
```

The answer is 0 because key 3 cannot open lock 1. A careless implementation that checks absolute difference incorrectly around boundaries could produce the wrong result.

A lock in the middle can be opened from either side, and having one matching neighbor is enough. For example:

```
1
4
1
5
```

The answer is 1 because key 4 opens lock 5. An implementation that requires both adjacent keys to exist would incorrectly return 0.

A key should not be confused with the lock being queried. For example:

```
1
10
1
10
```

The answer is 0 because key 10 does not open lock 10. It only opens 9. A direct membership check of the lock inside the key set would silently fail on this case.

## Approaches

The straightforward approach is to examine every lock and compare it with every key. For each queried lock, we would calculate the difference between that lock and every available key and count it if the difference is exactly one. This is correct because the unlocking rule depends only on that distance.

However, the worst case contains 100,000 keys and 100,000 locks. The brute-force method performs about 10 billion comparisons. Even with very fast operations, this amount of work cannot finish within the time limit.

The useful observation is that a lock does not care about all keys. It only cares about the two possible neighbors: the number immediately before it and the number immediately after it. Instead of searching through the whole key collection, we can store all keys in a hash set and directly ask whether either neighbor exists.

The brute-force solution works because it checks every possible relationship between a key and a lock, but it repeats a huge amount of unnecessary work. The observation that every lock has only two candidates reduces each query to two constant-time lookups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(kL) | O(1) | Too slow |
| Optimal | O(k + L) | O(k) | Accepted |

## Algorithm Walkthrough

1. Store every key number in a hash set. A set is used because we need to repeatedly check whether a particular number exists, and average O(1) lookup gives the required speed.
2. Read each active lock one at a time. We do not need to sort the locks or store them because each lock can be answered independently.
3. For the current lock `x`, check whether `x - 1` is in the key set or whether `x + 1` is in the key set. If either lookup succeeds, increment the answer.
4. Output the final count after all locks have been processed.

Why it works: every possible key that can open lock `x` must have a number exactly one smaller or exactly one larger than `x`. The algorithm checks exactly these two possibilities and no others. If one of them exists, the lock is counted, and if neither exists, no valid key exists. Since every queried lock is handled independently, the accumulated count is exactly the number of successful days.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input())
    keys = set(map(int, input().split()))

    L = int(input())
    locks = list(map(int, input().split()))

    ans = 0

    for lock in locks:
        if lock - 1 in keys or lock + 1 in keys:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The key set is built first because all later operations are membership checks. Python's set implementation provides average constant-time lookup, which is the core optimization.

Each lock is processed once. The code checks the two neighboring numbers directly instead of searching through all keys. The boundary cases are naturally handled because a lookup for a nonexistent number simply returns false. For example, checking `lock - 1` when `lock` is 1 tests 0, which cannot appear in the key set.

Python integers do not overflow here because the largest value is only 1,000,000,000, which is well within Python's integer representation.

## Worked Examples

### Sample 1

Input:

```
5
2 4 6 8 10
3
1 5 102
```

The algorithm builds the key set `{2, 4, 6, 8, 10}`.

| Lock | Check left neighbor | Check right neighbor | Count |
| --- | --- | --- | --- |
| 1 | 0 is absent | 2 is present | 1 |
| 5 | 4 is present | 6 is present | 2 |
| 102 | 101 is absent | 103 is absent | 2 |

The trace shows that only one matching neighbor is required. Lock 5 is counted even though both neighbors exist, while lock 102 fails because neither possible key exists.

### Custom Example

Input:

```
3
1 7 100
4
2 6 7 101
```

| Lock | Check left neighbor | Check right neighbor | Count |
| --- | --- | --- | --- |
| 2 | 1 is present | 3 is absent | 1 |
| 6 | 5 is absent | 7 is present | 2 |
| 7 | 6 is absent | 8 is absent | 2 |
| 101 | 100 is present | 102 is absent | 3 |

The trace confirms that a key with the same number as the lock does not help. Lock 7 is not opened by key 7.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k + L) | Every key is inserted once and every lock performs two set lookups. |
| Space | O(k) | The hash set stores all available keys. |

The largest input contains 100,000 keys and 100,000 locks. The linear solution performs only a few hundred thousand operations, which fits comfortably within the time limit and memory limit.

## Test Cases

```python
import sys
import io

def solve():
    import sys
    input = sys.stdin.readline

    k = int(input())
    keys = set(map(int, input().split()))
    L = int(input())
    locks = list(map(int, input().split()))

    ans = 0
    for lock in locks:
        if lock - 1 in keys or lock + 1 in keys:
            ans += 1

    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""5
2 4 6 8 10
3
1 5 102
""") == "2\n", "sample 1"

assert run("""1
1
1
2
""") == "1\n", "minimum values"

assert run("""4
1 3 5 7
5
2 4 6 8 10
""") == "4\n", "all locks except last have neighbors"

assert run("""3
999999998 999999999 1000000000
4
1 999999997 999999999 1000000000
""") == "3\n", "large boundary values"

assert run("""5
10 20 30 40 50
5
10 20 30 40 50
""") == "0\n", "same key and lock numbers do not match"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum key and lock values | 1 | Checks the smallest possible positions. |
| Alternating keys and locks | 4 | Confirms that each lock is judged by neighboring keys only. |
| Very large numbers | 3 | Checks the upper boundary near 1,000,000,000. |
| Identical key and lock positions | 0 | Prevents counting equal numbers as valid keys. |

## Edge Cases

For the boundary case, consider:

```
1
3
1
1
```

The key set contains only 3. The algorithm checks lock 1 by looking at 0 and 2. Neither exists, so the answer remains 0. It never assumes that a key with number 0 exists.

For the single-neighbor case:

```
1
4
1
5
```

The algorithm checks lock 5. The left neighbor, 4, is found in the set, so the answer becomes 1. It does not require the right neighbor to exist.

For the equal-number case:

```
1
10
1
10
```

The algorithm checks 9 and 11. Neither number is present, so the answer is 0. The lock number itself is irrelevant unless it also appears as a neighboring key, which is impossible.
