---
title: "CF 106447A - \u0411\u0438\u0431\u0438 \u0438 \u0435\u0433\u043e \u043f\u0430\u043f\u0430"
description: "The task simulates inserting numbers into a small hash table. The table has a fixed number of buckets, and a number x is assigned to the bucket x mod p. Each bucket can store only one number."
date: "2026-06-25T09:23:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106447
codeforces_index: "A"
codeforces_contest_name: "\u041a\u043e\u0433\u043d\u0438\u0442\u0438\u0432\u043d\u044b\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438 2025-2026. \u0424\u0438\u043d\u0430\u043b"
rating: 0
weight: 106447
solve_time_s: 32
verified: true
draft: false
---

[CF 106447A - \u0411\u0438\u0431\u0438 \u0438 \u0435\u0433\u043e \u043f\u0430\u043f\u0430](https://codeforces.com/problemset/problem/106447/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 32s  
**Verified:** yes  

## Solution
## Problem Understanding

The task simulates inserting numbers into a small hash table. The table has a fixed number of buckets, and a number `x` is assigned to the bucket `x mod p`. Each bucket can store only one number. The numbers arrive one by one in the given order, and we must find the first position where an insertion tries to use a bucket that already contains another number. If every insertion goes into an empty bucket, the answer is `-1`.

The input gives the number of buckets `p`, the number of values to insert `n`, and then the sequence of values. The output is the 1-based index of the first conflicting insertion.

The constraints are small, with both `p` and `n` limited to 300. This means even a simple simulation is easily fast enough. The number of insertions is only a few hundred, so algorithms with linear or quadratic behavior would both fit. There is no need for advanced hashing structures because the whole table is tiny.

The main edge cases come from the order of insertions and from values that look different but map to the same bucket. For example, with:

```
5 3
1
6
11
```

the correct output is:

```
2
```

because `1 mod 5`, `6 mod 5`, and `11 mod 5` are all equal to `1`. The second insertion is already a conflict. A careless implementation that stores the original numbers instead of the bucket positions would incorrectly think all three values are different.

Another case is when all buckets are filled without conflict:

```
4 4
0
1
2
3
```

The correct output is:

```
-1
```

A solution that assumes the last insertion must fail would be wrong. A full table is still valid if every value was inserted into a unique bucket.

A final boundary case is when the same value appears twice:

```
10 2
123456789
123456789
```

The correct output is:

```
2
```

The second value maps to exactly the same bucket as the first one. Comparing only whether the original values are repeated is unnecessary because collisions can also happen between different values.

## Approaches

The brute-force approach is to simulate the hash table exactly as described. Maintain the current contents of every bucket. For each incoming number, compute its bucket index using the remainder operation and check whether that bucket is already occupied. If it is empty, mark it as used and continue. If it is occupied, the current position is the answer.

This method is correct because the problem asks for the first conflict in the actual insertion order, and the simulation follows that order directly. The worst case performs `n` insertions and one constant-time check for each insertion, so even the direct implementation only needs about 300 operations.

The key insight is that the hash table itself is the only state that matters. Once a value has been converted into its bucket index, the original number no longer affects future decisions. We do not need to store the numbers at all, only whether each bucket has already received an element.

The brute-force simulation and the optimal solution are effectively the same idea here. The optimization is recognizing that the state can be represented by a simple boolean array of size `p`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(p) | Accepted |
| Optimal | O(n) | O(p) | Accepted |

## Algorithm Walkthrough

1. Create an array representing the buckets of the hash table. Each position stores whether that bucket has already been used.
2. Read each number in the order it appears. Compute its bucket index as `x mod p`.
3. Check the corresponding bucket. If it is already occupied, output the current insertion position because this is the first conflict.
4. If the bucket is empty, mark it as occupied and continue processing the next number.
5. If all numbers are processed without finding a conflict, output `-1`.

The reason this works is that every future insertion only depends on which buckets are occupied, not on which values created those occupied buckets. Keeping exactly this information is enough to reproduce the behavior of the hash table.

Why it works: after processing the first `i` values, the bucket array exactly matches the real hash table after `i` insertions. For the next value, the algorithm checks the same bucket that the real insertion would use. If it is occupied, both the real process and the algorithm detect a conflict at this step. If it is empty, both mark it as filled and continue. Since the invariant holds after every insertion, the first reported conflict is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    p, n = map(int, input().split())
    used = [False] * p

    for i in range(1, n + 1):
        x = int(input())
        bucket = x % p

        if used[bucket]:
            print(i)
            return

        used[bucket] = True

    print(-1)

if __name__ == "__main__":
    solve()
```

The array `used` represents the hash table buckets. Its size is exactly `p`, so every possible bucket index has a corresponding position.

The loop starts from `1` because the answer is based on the insertion number, not a zero-based array index. Before marking a bucket as occupied, the code checks whether it was already used. This order matters because changing the value first would hide the conflict.

Python integers handle the large input values directly, so there is no need for special handling of overflow. The modulo operation immediately reduces every value to a valid bucket index between `0` and `p - 1`.

## Worked Examples

### Sample 1

Input:

```
10 5
0
21
53
41
53
```

| Step | Value | Bucket | Bucket used before? | Action | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | No | Mark bucket 0 | Continue |
| 2 | 21 | 1 | No | Mark bucket 1 | Continue |
| 3 | 53 | 3 | No | Mark bucket 3 | Continue |
| 4 | 41 | 1 | Yes | Conflict found | 4 |

The trace shows why the algorithm stores buckets instead of values. The values `21` and `41` are different, but they collide because they both map to bucket `1`.

### Sample 2

Input:

```
5 5
0
1
2
3
4
```

| Step | Value | Bucket | Bucket used before? | Action | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | No | Mark bucket 0 | Continue |
| 2 | 1 | 1 | No | Mark bucket 1 | Continue |
| 3 | 2 | 2 | No | Mark bucket 2 | Continue |
| 4 | 3 | 3 | No | Mark bucket 3 | Continue |
| 5 | 4 | 4 | No | Mark bucket 4 | -1 |

This demonstrates that filling every bucket does not imply a collision. The answer is only about whether an insertion attempts to reuse an existing bucket.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each number is processed once with a constant-time modulo and lookup operation. |
| Space | O(p) | The algorithm stores one boolean value for each bucket. |

The maximum input size is very small, so this approach easily fits the time and memory limits. It also scales linearly if the number of insertions is increased.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    data = inp.strip().split()
    if not data:
        return ""

    p = int(data[0])
    n = int(data[1])
    used = [False] * p

    index = 2
    for i in range(1, n + 1):
        x = int(data[index])
        index += 1
        bucket = x % p
        if used[bucket]:
            return str(i)
        used[bucket] = True

    return "-1"

# provided samples
assert solution("""10 5
0
21
53
41
53
""") == "4", "sample 1"

assert solution("""5 5
0
1
2
3
4
""") == "-1", "sample 2"

# custom cases
assert solution("""2 2
0
2
""") == "2", "same bucket collision"

assert solution("""3 3
1000000000
1000000001
1000000002
""") == "-1", "large values with unique buckets"

assert solution("""10 4
7
17
27
37
""") == "2", "repeated bucket pattern"

assert solution("""300 1
299999999
""") == "-1", "single insertion boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two values with the same remainder | 2 | Detecting immediate collisions |
| Large numbers with different remainders | -1 | Correct modulo handling |
| Several values sharing one bucket | 2 | Stopping at the first conflict |
| One insertion | -1 | Minimum input handling |

## Edge Cases

For the case where different values collide, such as:

```
5 3
1
6
11
```

the algorithm processes `1` and marks bucket `1`. When it reaches `6`, it computes `6 mod 5 = 1`, sees that bucket `1` is already occupied, and immediately outputs `2`. It never needs to inspect the remaining values because the first conflict has already been found.

For a completely valid table filling:

```
4 4
0
1
2
3
```

each value maps to a different bucket. The algorithm marks buckets `0`, `1`, `2`, and `3` in order. No occupied bucket is encountered, so after the loop it returns `-1`.

For repeated values:

```
10 2
123456789
123456789
```

the first insertion marks bucket `9`. The second insertion computes the same bucket index and finds it occupied. The algorithm reports `2`, matching the required first conflict position.
