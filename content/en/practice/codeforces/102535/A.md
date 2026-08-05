---
title: "CF 102535A - Working With Locks"
description: "We have a small collection of five keys and five locks. The input gives the number of the key Perry owns and the number of the lock on the door. The task is to decide whether that particular key is capable of opening that particular lock."
date: "2026-08-05T15:11:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102535
codeforces_index: "A"
codeforces_contest_name: "2020 UP ACM Algolympics Elimination Round"
rating: 0
weight: 102535
solve_time_s: 640
verified: true
draft: false
---

[CF 102535A - Working With Locks](https://codeforces.com/problemset/problem/102535/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a small collection of five keys and five locks. The input gives the number of the key Perry owns and the number of the lock on the door. The task is to decide whether that particular key is capable of opening that particular lock. If the key works, we print the success message, otherwise we print the failure message.

The relationship between keys and locks is fixed. Key 1 works only with lock 2, key 2 works with locks 1 and 3, key 3 works with locks 2 and 4, key 4 works with locks 3 and 5, and key 5 works only with lock 4. Since there are only five possible keys and five possible locks, the entire decision space contains just 25 combinations. The constraints do not require any advanced data structure or optimization. Any solution that performs a constant amount of work is easily fast enough.

The main edge cases come from the ends of the key sequence and from assuming that nearby numbers always work in the same direction. For example, the input

```
1
4
```

should produce:

```
CURSE YOU
```

Key 1 only opens lock 2, so treating the keys as if they could open all locks within some distance would give an incorrect result.

Another boundary case is the last key:

```
5
4
```

The correct output is:

```
GOOD LUCK AGENT P
```

Key 5 has only one valid lock, and that lock is 4. An implementation that tries to access a nonexistent lock 6 while checking neighboring locks could fail.

A third case is when the key and lock have the same number:

```
3
3
```

The correct output is:

```
CURSE YOU
```

The numbers identify different objects. The key number matching the lock number does not imply compatibility.

## Approaches

A straightforward approach is to store the possible locks for each key and check whether the given lock appears in that list. This is effectively a direct simulation of the lock system. It is correct because every valid key-lock pair is checked against the exact rules. In this problem, the worst case still requires checking only two possible locks for one key, so it performs at most a few operations.

A more general brute-force interpretation would be to try every possible key and lock relationship until the given pair is found. With five keys and five locks, that means checking at most 25 pairs. This is also easily acceptable here, but it ignores the fact that the input already identifies the only pair we care about.

The key observation is that the lock system is static. The answer does not depend on any calculation or search. It only depends on whether the pair belongs to a small predefined set of valid pairs. Representing those pairs directly turns the problem into a constant-time membership check.

The brute-force approach works because the input size is tiny, but it does not express the actual structure of the problem. The observation that the valid relationships are fixed lets us reduce the solution to a single lookup.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(25) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the key number and the lock number from the input. These two values completely describe the situation we need to evaluate.
2. Create a representation of the valid key-lock pairs. The representation maps each key to the locks it can open, matching the rules of the lock system.
3. Check whether the given lock exists among the locks available for the given key. A successful lookup means the key can open the door.
4. Print `"GOOD LUCK AGENT P"` for a valid pair and `"CURSE YOU"` otherwise.

Why it works:

The stored mapping contains exactly every key-lock relationship that is allowed. For any input, the algorithm checks the same condition as the problem definition: whether the provided lock belongs to the set of locks opened by the provided key. Since no valid pair is missing and no invalid pair is included, the answer produced by the lookup is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input())
    L = int(input())

    can_open = {
        1: {2},
        2: {1, 3},
        3: {2, 4},
        4: {3, 5},
        5: {4}
    }

    if L in can_open[k]:
        print("GOOD LUCK AGENT P")
    else:
        print("CURSE YOU")

if __name__ == "__main__":
    solve()
```

The dictionary stores the complete lock system. Each key number points to a set containing exactly the lock numbers that it can open.

The membership check uses the given key to retrieve its possible locks and then checks whether the input lock is inside that set. Since the input values are guaranteed to be between 1 and 5, there is no need for additional validation or boundary handling.

There are no indexing calculations, so there are no off-by-one risks. The solution also avoids arithmetic assumptions about the relationship between key and lock numbers, which is important because the first and last keys behave differently from the middle keys.

## Worked Examples

For Sample 1:

```
1
4
```

| Step | Key | Lock | Available locks for key | Result |
| --- | --- | --- | --- | --- |
| Read input | 1 | 4 | {2} | Continue |
| Check membership | 1 | 4 | {2} | 4 is not present |
| Output | 1 | 4 | {2} | CURSE YOU |

The trace shows that equal or nearby numbers do not determine compatibility. The answer comes only from the predefined relationships.

For Sample 2:

```
2
3
```

| Step | Key | Lock | Available locks for key | Result |
| --- | --- | --- | --- | --- |
| Read input | 2 | 3 | {1, 3} | Continue |
| Check membership | 2 | 3 | {1, 3} | 3 is present |
| Output | 2 | 3 | {1, 3} | GOOD LUCK AGENT P |

This example confirms that a key can open more than one lock and that the lookup handles multiple valid choices correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The algorithm performs one dictionary lookup and one membership test. |
| Space | O(1) | The mapping contains a fixed number of entries regardless of input size. |

The constraints are extremely small, so the constant-time solution easily fits within the time limit and memory limit. The same approach would remain efficient even if the number of test cases increased significantly.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    k = int(sys.stdin.readline())
    L = int(sys.stdin.readline())

    can_open = {
        1: {2},
        2: {1, 3},
        3: {2, 4},
        4: {3, 5},
        5: {4}
    }

    if L in can_open[k]:
        print("GOOD LUCK AGENT P")
    else:
        print("CURSE YOU")

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

assert solution("1\n4\n") == "CURSE YOU\n", "sample 1"
assert solution("2\n3\n") == "GOOD LUCK AGENT P\n", "sample 2"
assert solution("3\n1\n") == "CURSE YOU\n", "sample 3"

assert solution("1\n2\n") == "GOOD LUCK AGENT P\n", "minimum key boundary"
assert solution("5\n4\n") == "GOOD LUCK AGENT P\n", "maximum key boundary"
assert solution("5\n5\n") == "CURSE YOU\n", "same value but invalid pair"
assert solution("3\n4\n") == "GOOD LUCK AGENT P\n", "middle key upper boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n2\n` | `GOOD LUCK AGENT P` | Checks the smallest key with its only valid lock. |
| `5\n4\n` | `GOOD LUCK AGENT P` | Checks the largest key and its boundary relationship. |
| `5\n5\n` | `CURSE YOU` | Prevents assuming equal numbers always match. |
| `3\n4\n` | `GOOD LUCK AGENT P` | Checks a middle key with a valid higher lock. |

## Edge Cases

For the first boundary case:

```
1
4
```

The algorithm retrieves the set `{2}` for key 1. The membership check asks whether 4 exists in that set, which is false, so it prints `CURSE YOU`. This handles the case where a key has only one possible lock and avoids accepting unrelated locks.

For the last key:

```
5
4
```

The algorithm retrieves `{4}` for key 5. The value 4 is found immediately, so the output is `GOOD LUCK AGENT P`. The fixed mapping prevents any attempt to look beyond the available key range.

For matching numbers:

```
3
3
```

The algorithm retrieves `{2, 4}` for key 3. Since 3 is not present, it prints `CURSE YOU`. This confirms that the solution checks actual compatibility instead of comparing the two input numbers directly.

I can also adapt this editorial into a shorter Codeforces-style version if you want something closer to an actual contest submission explanation.
