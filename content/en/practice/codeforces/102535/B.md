---
title: "CF 102535B - Working with Locks 2"
description: "We have a collection of key numbers and a collection of lock numbers. A key opens a lock only when the two numbers are adjacent, meaning their absolute difference is exactly one. The task is to count how many of the given locks have at least one usable key."
date: "2026-08-06T19:48:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102535
codeforces_index: "B"
codeforces_contest_name: "2020 UP ACM Algolympics Elimination Round"
rating: 0
weight: 102535
solve_time_s: 74
verified: true
draft: false
---

[CF 102535B - Working with Locks 2](https://codeforces.com/problemset/problem/102535/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of key numbers and a collection of lock numbers. A key opens a lock only when the two numbers are adjacent, meaning their absolute difference is exactly one. The task is to count how many of the given locks have at least one usable key.

The input describes the keys Perry owns and the locks that appear during the active days. The first part gives the distinct key numbers, and the second part gives the distinct lock numbers. The output is the number of locks that can be opened by the available keys.

The values are limited to 104, but the amount of keys and locks can each also reach 104. This means a solution that checks every key against every lock performs up to 10^8 comparisons in the worst case. That is close to the limit of what might pass in some languages, but it is unnecessary here because the number range is small and the relationship between keys and locks has a very simple structure. A linear approach is easily fast enough.

The main edge cases come from the ends of the number range and from forgetting that a lock needs only one matching key. For example, with the input

```
1
1
1
1
```

the answer is `0`. A key numbered 1 cannot open lock 1 because the difference is zero, not one.

Another boundary case is:

```
1
1
1
2
```

The answer is `1`. The only key is exactly one away from the lock, so it works. An implementation that only checks the previous number for a lock would fail here.

A similar upper-bound case is:

```
1
104
1
103
```

The answer is `1`. Key 104 can open lock 103, so the last value in the range behaves the same way as all other values.

## Approaches

The direct solution is to examine every lock and compare it with every key. For a particular lock, if any key has a difference of exactly one, that lock contributes one to the answer. This method is correct because it directly follows the definition of a valid key. However, with 10^4 keys and 10^4 locks, it can perform around 10^8 checks, which is much more work than needed.

The structure of the problem gives us a simpler observation. A lock with number x can only be opened by keys x - 1 and x + 1. We never need to search through all keys. Instead, we can store the available keys in a set, then each lock can be checked by performing two constant-time membership queries.

The brute-force method works because it explores every possible key-lock pair, but it fails because almost all of those pairs are irrelevant. The observation that each lock has only two possible useful keys reduces the problem to a sequence of simple lookups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(kL) | O(1) | Too slow for the largest input |
| Optimal | O(k + L) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read all key numbers and store them in a set. The set allows us to ask whether a particular key exists without scanning the whole collection.
2. For every lock number x, check whether x - 1 exists in the key set or x + 1 exists in the key set. These are the only two possible keys that can open this lock.
3. Increase the answer whenever at least one of those two possible keys is present.
4. Print the final count of successful locks.

The reason this works is that the opening rule depends only on the distance between the key and lock numbers. For any lock x, every key other than x - 1 and x + 1 has a distance different from one, so checking those two values covers every possible successful case.

Why it works:

The invariant maintained while processing locks is that the answer equals the number of already processed locks that have at least one adjacent key in the set. When a new lock x is examined, the algorithm checks exactly the complete set of possible keys that could open it. If one exists, the count increases, and if none exists, the count stays unchanged. Thus every lock is counted exactly when it should be.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    idx = 0

    k = int(data[idx])
    idx += 1

    keys = set()
    for _ in range(k):
        keys.add(int(data[idx]))
        idx += 1

    L = int(data[idx])
    idx += 1

    answer = 0
    for _ in range(L):
        lock = int(data[idx])
        idx += 1
        if lock - 1 in keys or lock + 1 in keys:
            answer += 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The solution first creates a set from the keys because membership checks are the central operation. A Python set gives average O(1) lookup time, which turns each lock check into constant work.

The loop over locks follows the algorithm directly. For a lock value `lock`, the expressions `lock - 1` and `lock + 1` represent the only possible key numbers. The boundaries do not require special handling because looking up values outside the valid key range simply returns false from the set.

The implementation reads all input tokens at once because the input size is small and this avoids depending on whether the judge provides extra whitespace or line formatting. There is no integer overflow concern in Python, and the largest value checked is only 105.

## Worked Examples

For the provided sample:

```
5
2 4 6 8 10
3
1 5 102
```

The key set is `{2, 4, 6, 8, 10}`.

| Lock | Check lock - 1 | Check lock + 1 | Count after processing |
| --- | --- | --- | --- |
| 1 | 0 not found | 2 found | 1 |
| 5 | 4 found | 6 found | 2 |
| 102 | 101 not found | 103 not found | 2 |

The first lock works because key 2 opens it. The second lock has two possible keys, both of which exist. The last lock has no adjacent key, so the answer remains 2.

A second example:

```
3
1 50 104
4
2 49 103 104
```

The key set is `{1, 50, 104}`.

| Lock | Check lock - 1 | Check lock + 1 | Count after processing |
| --- | --- | --- | --- |
| 2 | 1 found | 3 not found | 1 |
| 49 | 48 not found | 50 found | 2 |
| 103 | 102 not found | 104 found | 3 |
| 104 | 103 not found | 105 not found | 3 |

This example exercises both directions of the adjacency rule and confirms that a key cannot open a lock with the same number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k + L) | Each key is inserted once and each lock is checked with two set lookups. |
| Space | O(k) | The set stores all available keys. |

The maximum input contains only 10^4 keys and 10^4 locks, so the linear solution performs roughly a few tens of thousands of operations. It is comfortably within the time and memory limits.

## Test Cases

```python
import sys
import io

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

# provided sample
assert run("""5
2 4 6 8 10
3
1 5 102
""") == "2\n", "sample 1"

# minimum-size case
assert run("""1
1
1
1
""") == "0\n", "same key and lock do not work"

# lower boundary
assert run("""1
1
1
2
""") == "1\n", "key 1 opens lock 2"

# upper boundary
assert run("""1
104
1
103
""") == "1\n", "key 104 opens lock 103"

# larger mixed case
assert run("""4
2 10 50 104
5
1 3 9 51 100
""") == "4\n", "checks both sides of every lock"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single key 1 and lock 1 | 0 | Same numbers are not valid pairs |
| Key 1 and lock 2 | 1 | Lower boundary adjacency |
| Key 104 and lock 103 | 1 | Upper boundary adjacency |
| Mixed values around several keys | 4 | General correctness of both directions |

## Edge Cases

For the case where a key and lock have the same number, such as:

```
1
1
1
1
```

the algorithm checks lock 1 by looking for keys 0 and 2. Neither exists, so the answer remains zero. This avoids the common mistake of treating equality as a valid match.

For a lock that is opened by the larger key, such as:

```
1
1
1
2
```

the algorithm checks keys 1 and 3 for lock 2. Key 1 exists, so the answer becomes one. This confirms that both directions of the difference rule are handled.

For the final boundary value:

```
1
104
1
103
```

the algorithm checks keys 102 and 104 for lock 103. Key 104 exists, so the lock is counted successfully. Values outside the allowed range do not cause a problem because they are simply absent from the set.
