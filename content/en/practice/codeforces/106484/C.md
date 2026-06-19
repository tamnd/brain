---
title: "CF 106484C - Bugcat's Unique Queue"
description: "We maintain a queue that behaves like a normal FIFO structure, but with one extra rule: every value can appear at most once at any time. The values that may be stored are integers from 1 to m, and we process Q operations that modify or query this structure."
date: "2026-06-19T15:16:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106484
codeforces_index: "C"
codeforces_contest_name: "2026 GBA International Programming Contest"
rating: 0
weight: 106484
solve_time_s: 47
verified: true
draft: false
---

[CF 106484C - Bugcat's Unique Queue](https://codeforces.com/problemset/problem/106484/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a queue that behaves like a normal FIFO structure, but with one extra rule: every value can appear at most once at any time. The values that may be stored are integers from 1 to m, and we process Q operations that modify or query this structure.

There are three operations. One tries to insert a value at the back of the queue, but only succeeds if the value is not already present. Another removes the element at the front, which is always valid because the queue is guaranteed to be non-empty when this operation appears. The last operation asks for the x-th element currently in the queue in front-to-back order, and if that position does not exist, the answer is −1.

The key subtlety is that we are not asked to simulate an arbitrary container, but a sequence with uniqueness constraints and positional queries. The constraints Q ≤ 10^6 and m ≤ 10^6 rule out any approach that scans the queue or checks membership by linear search per operation. Even a single O(n) operation repeated Q times would immediately exceed limits, since the queue size can grow to Q in the worst case.

A naive mistake is to represent the queue as a Python list and use `x in list` to enforce uniqueness. Another is to answer queries by indexing into a list but forgetting that deletions from the front shift everything, making that O(n) per pop.

A concrete failure case appears when the queue grows large and queries are frequent:

Input:

1 1

1 1

1 2

1 3

...

3 100000

A naive list-based solution would repeatedly scan for membership and shift elements on pop, leading to timeouts.

Another subtle bug arises from ignoring uniqueness: if we allow duplicates, a query for the first occurrence position becomes ambiguous and diverges from the intended model.

## Approaches

A brute-force simulation keeps the queue as a dynamic list. Insertion checks whether the value already exists by scanning the entire list. If not found, it appends to the end. Pop removes the first element by slicing or pop(0), and queries index directly.

The correctness is straightforward because it mirrors the operations exactly. The issue is performance. Membership checks cost O(n), and popping from the front also costs O(n) due to shifting. With Q up to 10^6 and queue size potentially growing linearly, the total work becomes O(Q^2), which is far beyond feasible limits.

The key observation is that we do not actually need to maintain a “list structure” in a shifting sense. We only need to preserve the relative order of elements and support three operations: append unique elements, remove the oldest element, and access by index in current order.

This suggests separating concerns: we track elements in a fixed array representing insertion order, and maintain a moving pointer for the front. Instead of physically removing elements, we advance a head index. To enforce uniqueness, we maintain a boolean array or hash set indicating whether a value is currently active in the queue. This reduces all operations to O(1).

The queue becomes a virtual window over an array, which removes all costly deletions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Q^2) | O(Q) | Too slow |
| Optimal | O(Q) | O(Q) | Accepted |

## Algorithm Walkthrough

We maintain three structures: an array `arr` storing inserted values in order, a pointer `head` marking the current front, and a boolean array `in_queue` indicating whether a value is currently inside the active queue window.

1. For an insertion operation with value x, we first check whether `in_queue[x]` is false. If it is false, we append x to `arr` and mark `in_queue[x] = true`. This ensures uniqueness without scanning the queue.
2. For a pop operation, we move `head` forward until we skip one active element. Concretely, we take the element at `arr[head]`, mark it as not in the queue, and increment `head`. This simulates removing the front in O(1) amortized time because each element is removed exactly once.
3. For a query operation asking for the x-th element, we compute the actual index as `head + x - 1`. If this index is beyond the current array length, we output −1. Otherwise, we output `arr[index]`. The reasoning is that the active queue is always a contiguous suffix of the processed array.

Why it works is based on the invariant that every element is either already permanently skipped by the head pointer or is still part of the active suffix of `arr`. No element re-enters the structure after removal, and no element appears twice because we maintain a strict active-set flag. Therefore, the queue state is always represented exactly by the segment `arr[head : len(arr)]`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    Q, m = map(int, input().split())
    
    arr = []
    in_queue = [False] * (m + 1)
    head = 0
    
    out = []
    
    for _ in range(Q):
        tmp = input().split()
        t = int(tmp[0])
        
        if t == 1:
            x = int(tmp[1])
            if not in_queue[x]:
                arr.append(x)
                in_queue[x] = True
        
        elif t == 2:
            x = arr[head]
            in_queue[x] = False
            head += 1
        
        else:
            x = int(tmp[1])
            idx = head + x - 1
            if idx >= len(arr):
                out.append("-1")
            else:
                out.append(str(arr[idx]))
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation stores all inserted values in a growing array and never physically deletes from the left. The `head` pointer replaces costly deque pops. The boolean array guarantees O(1) membership checks for insertion, so duplicates are never added.

One subtle point is that we never shrink `arr`. This is intentional: even though old elements remain in memory, they are ignored once `head` passes them. Queries rely only on index arithmetic, not structural mutation.

## Worked Examples

Consider the following sequence:

Input:

```
1 1
1 1
1 2
1 3
2
3 1
3 2
```

We track state:

| Step | Operation | arr | head | in_queue | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | insert 1 | [1] | 0 | {1} |  |
| 2 | insert 2 | [1,2] | 0 | {1,2} |  |
| 3 | insert 3 | [1,2,3] | 0 | {1,2,3} |  |
| 4 | pop | [1,2,3] | 1 | {2,3} |  |
| 5 | query 1 | [1,2,3] | 1 | {2,3} | 2 |
| 6 | query 2 | [1,2,3] | 1 | {2,3} | 3 |

This shows that logical queue content is always the suffix starting at `head`.

Now consider duplicate prevention:

Input:

```
1 5
1 1
1 2
1 1
3 2
```

| Step | Operation | arr | head | in_queue | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | insert 1 | [1] | 0 | {1} |  |
| 2 | insert 2 | [1,2] | 0 | {1,2} |  |
| 3 | insert 1 | [1,2] | 0 | {1,2} |  |
| 4 | query 2 | [1,2] | 0 | {1,2} | 2 |

The second insertion of 1 is ignored, preserving uniqueness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Q) | Each element is inserted once, removed once, and queried in O(1) |
| Space | O(Q + m) | Array stores at most Q elements, boolean array tracks m values |

The constraints allow up to one million operations, so linear time processing with constant work per operation fits comfortably within the limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    Q, m = map(int, sys.stdin.readline().split())
    arr = []
    in_queue = [False] * (m + 1)
    head = 0
    out = []
    
    for _ in range(Q):
        tmp = sys.stdin.readline().split()
        t = int(tmp[0])
        
        if t == 1:
            x = int(tmp[1])
            if not in_queue[x]:
                arr.append(x)
                in_queue[x] = True
        
        elif t == 2:
            x = arr[head]
            in_queue[x] = False
            head += 1
        
        else:
            x = int(tmp[1])
            idx = head + x - 1
            out.append(str(arr[idx]) if idx < len(arr) else "-1")
    
    return "\n".join(out)

# sample-like test
assert run("""10 10
1 3
1 5
3 1
3 2
1 3
1 5
1 8
3 2
3 3
1 2
""") == "3\n5\n5\n8", "sample-like"

# minimum case
assert run("""1 1
3 1
""") == "-1", "min query empty"

# duplicate prevention
assert run("""5 3
1 1
1 1
1 2
3 2
3 1
""") == "2\n1", "duplicates ignored"

# full pop then query
assert run("""6 5
1 1
1 2
2
2
3 1
""") == "-1", "empty queue after pops"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample-like | 3 5 5 8 | basic operations + query correctness |
| min query empty | -1 | querying empty structure |
| duplicates ignored | 2 1 | uniqueness enforcement |
| full pop then query | -1 | boundary after deletions |

## Edge Cases

One important edge case is repeated insertion of the same value without removal. For example:

Input:

```
1 5
1 1
1 1
1 1
3 1
```

The algorithm keeps only one instance of value 1 because `in_queue[1]` blocks all repeats. The queue state is `[1]`, so query returns 1.

Another edge case is querying beyond current size after many pops:

Input:

```
1 3
1 1
1 2
2
3 2
```

After the pop, only `[2]` remains. Querying the second element computes `head + 1`, which exceeds `len(arr)`, so the answer is −1. The pointer-based representation ensures we never access invalid memory; bounds are checked purely arithmetically.

A final edge case is maximal input stress where all operations are inserts followed by queries. Because no deletion is physical, the array grows but remains valid for O(Q) memory, and all queries are resolved in constant time.
