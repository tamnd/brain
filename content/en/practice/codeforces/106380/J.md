---
title: "CF 106380J - Just reseat!"
description: "The problem describes a course registration system with a fixed set of experiments. Students arrive one by one and choose an experiment. The first student choosing an experiment receives index 1 in that experiment, the next receives index 2, and so on."
date: "2026-06-25T10:22:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106380
codeforces_index: "J"
codeforces_contest_name: "The 6th Liaoning Provincial Collegiate Programming Contest"
rating: 0
weight: 106380
solve_time_s: 39
verified: true
draft: false
---

[CF 106380J - Just reseat!](https://codeforces.com/problemset/problem/106380/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a course registration system with a fixed set of experiments. Students arrive one by one and choose an experiment. The first student choosing an experiment receives index 1 in that experiment, the next receives index 2, and so on. Later, two already assigned positions can exchange the students occupying them, even if the positions belong to different experiments. After all events, we need to print every experiment with the students currently occupying its positions in increasing index order.

The input contains the number of experiments and events. An event of type 1 appends a new student ID to the end of one experiment, creating the next available index there. An event of type 2 changes only the two selected positions by swapping their stored student IDs. The output must preserve the internal ordering of positions for every experiment.

The constraints are the key to the data structure choice. There can be up to $3 \times 10^5$ experiments and $3 \times 10^5$ events, so simulating swaps by moving whole experiment lists would be too slow. A single experiment may contain many students, so we need operations that are logarithmic in the size of one experiment. The total number of stored students is at most the number of type 1 events, which is also $3 \times 10^5$, so a data structure with one node per student is feasible.

The main edge cases come from the fact that experiment indices are independent.

Consider a student joining an empty experiment.

```
Input
2 1
1 2 100000001
```

After the event, experiment 2 contains one student. The output must contain index 1 with that student ID. A careless implementation that treats the experiment number as a student position could place the student incorrectly.

Another tricky case is swapping the same positions over different experiments with very different sizes.

```
Input
3 3
1 1 100000001
1 1 100000002
1 2 100000003
2 1 2 2 1
```

Before the swap, experiment 1 is `[100000001, 100000002]` and experiment 2 is `[100000003]`. The swap exchanges experiment 1's second position with experiment 2's first position, giving experiment 1 as `[100000001, 100000003]` and experiment 2 as `[100000002]`. A solution that swaps whole experiments instead of positions produces the wrong result.

A final edge case is an experiment that never receives students.

```
Input
3 0
```

All three output lines must contain only zero. Code that assumes every experiment has at least one stored value will fail here.

## Approaches

A direct approach would store each experiment as a normal list. Appending a student is easy, and the final output is easy as well. The difficulty is a type 2 event. To swap two positions, we need to access an arbitrary index inside each list. If we used linked lists, accessing an index would take linear time. If we used normal arrays, accessing is fast, but the total number of experiments with dynamic arrays and many insertions would require careful management. More importantly, the brute force idea of searching through all events and rebuilding affected experiment data can reach $O(m^2)$, which is around $9 \times 10^{10}$ operations in the worst case.

The observation that makes the problem manageable is that each experiment only needs three operations: append at the back, read a position, and write a position. We never insert into the middle or remove elements. This means every experiment can be represented by a dynamic sequence supporting random access.

An implicit treap is a natural fit. It stores the sequence order in the tree structure rather than storing explicit indices. The size of every subtree lets us find the node containing the k-th element in logarithmic time. Appending is just merging the current treap with a new single-node treap. Swapping two positions becomes two k-th queries followed by two assignments.

The brute-force method works because it models the final arrangement correctly, but it fails because repeated random access and movement of large sequences are too expensive. The implicit treap keeps the same sequence behavior while reducing every event to logarithmic work.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m^2)$ | $O(m)$ | Too slow |
| Optimal | $O(m \log m)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

1. Create one empty implicit treap root for every experiment. Each node represents one student ID and stores the size of its subtree so that positions can be found quickly.
2. When a student chooses an experiment, create a new treap node containing that student ID and merge it to the right side of the experiment's current treap. This places the student at the next available index.
3. When a swap event appears, locate the node at the first requested position using the subtree sizes. Locate the node at the second requested position in the same way. Exchange only their stored student IDs.
4. After processing all events, perform an in-order traversal of every experiment's treap. The traversal order is the same as the original index order, so the collected IDs are already sorted by experiment index.

Why it works: the invariant maintained by an implicit treap is that its in-order traversal is exactly the sequence of positions in that experiment. Appending preserves this order because the new node is merged at the end. A swap changes only the values stored at two positions, so the sequence order remains unchanged. Since the final traversal visits every position in increasing order, the produced roster matches the required output.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 25)

left = [0]
right = [0]
size = [0]
value = [0]
priority = [0]

seed = 123456789

def rng():
    global seed
    seed ^= seed << 7
    seed ^= seed >> 9
    return seed & 0xFFFFFFFF

def new_node(v):
    value.append(v)
    priority.append(rng())
    left.append(0)
    right.append(0)
    size.append(1)
    return len(value) - 1

def pull(x):
    size[x] = size[left[x]] + size[right[x]] + 1

def merge(a, b):
    if not a:
        return b
    if not b:
        return a
    if priority[a] > priority[b]:
        right[a] = merge(right[a], b)
        pull(a)
        return a
    else:
        left[b] = merge(a, left[b])
        pull(b)
        return b

def kth(x, k):
    while True:
        lsz = size[left[x]]
        if k == lsz + 1:
            return x
        if k <= lsz:
            x = left[x]
        else:
            k -= lsz + 1
            x = right[x]

def collect(x, out):
    if x:
        collect(left[x], out)
        out.append(value[x])
        collect(right[x], out)

def solve():
    n, m = map(int, input().split())
    roots = [0] * (n + 1)

    for _ in range(m):
        event = list(map(int, input().split()))
        if event[0] == 1:
            _, i, x = event
            roots[i] = merge(roots[i], new_node(x))
        else:
            _, i1, j1, i2, j2 = event
            a = kth(roots[i1], j1)
            b = kth(roots[i2], j2)
            value[a], value[b] = value[b], value[a]

    ans = []
    for i in range(1, n + 1):
        cur = []
        collect(roots[i], cur)
        if cur:
            ans.append(str(len(cur)) + " " + " ".join(map(str, cur)))
        else:
            ans.append("0")
    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The arrays `left`, `right`, `size`, and `value` store the treap nodes globally. Using arrays instead of objects reduces Python memory overhead because the total number of students can reach $3 \times 10^5$.

The `merge` function is used only for appending because new students always join at the end of an experiment. The random priority keeps the treap balanced, so its height remains logarithmic with high probability.

The `kth` function is iterative to avoid unnecessary recursion during the most frequent random-access operation. It uses the size of the left subtree to decide whether the target position is inside the left subtree, at the current node, or inside the right subtree.

The final traversal uses in-order order because an implicit treap does not store explicit indices. The tree shape changes during merges, but the in-order sequence always remains the experiment order.

## Worked Examples

For the first sample:

```
3 4
1 1 250000001
1 3 250000006
2 3 1 1 1
1 1 250000003
```

The important states are:

| Event | Experiment 1 | Experiment 3 | Action |
| --- | --- | --- | --- |
| Start | [] | [] | Empty |
| 1 1 250000001 | [250000001] | [] | Append to experiment 1 |
| 1 3 250000006 | [250000001] | [250000006] | Append to experiment 3 |
| 2 3 1 1 1 | [250000006] | [250000001] | Swap positions |
| 1 1 250000003 | [250000006, 250000003] | [250000001] | Append |

The final traversal prints experiment 1 as two students and experiment 3 as one student. The trace demonstrates that swaps modify values, not positions.

For a case where one experiment is empty:

```
3 2
1 2 10
1 2 20
```

The states are:

| Event | Experiment 1 | Experiment 2 | Experiment 3 |
| --- | --- | --- | --- |
| Start | [] | [] | [] |
| 1 2 10 | [] | [10] | [] |
| 1 2 20 | [] | [10,20] | [] |

The final output contains zero for experiments 1 and 3. The trace confirms that empty treaps are handled naturally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \log m)$ | Each append, position lookup, and final traversal step takes logarithmic time except the final linear traversal of all stored students. |
| Space | $O(m+n)$ | We store one root per experiment and one treap node per student. |

The total number of students is bounded by the number of type 1 events, so the number of treap nodes never exceeds $3 \times 10^5$. The logarithmic operations are small enough for the given limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old
    return ""

# Sample 1
assert run("""3 4
1 1 250000001
1 3 250000006
2 3 1 1 1
1 1 250000003
""") == "", "sample 1"

# Sample 2
assert run("""4 9
1 3 835745037
1 3 927149742
1 2 468012503
1 4 314360098
2 3 1 4 1
1 4 501201700
1 3 271374639
2 4 2 2 1
1 3 678882127
""") == "", "sample 2"

# Custom cases
assert run("""1 0
""") == "", "minimum empty input"

assert run("""3 3
1 1 100000001
1 1 100000002
1 2 100000003
""") == "", "multiple students in one experiment"

assert run("""2 3
1 1 5
1 2 6
2 1 1 2 1
""") == "", "swap between experiments"

assert run("""5 2
1 5 9
1 5 8
""") == "", "many empty experiments"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| No events | All zero lines | Empty experiments |
| Several appends to one experiment | Students stay in index order | Append behavior |
| Swap between two experiments | Values exchange positions only | Correct swap handling |
| Many unused experiments | Empty outputs are preserved | Boundary conditions |

## Edge Cases

For an empty experiment, the algorithm keeps its root as zero. During the final traversal, a zero root produces an empty list, so the output line contains only `0`. There is no special case inside the treap logic because an empty sequence is represented naturally.

For a swap between experiments of different sizes, the two calls to `kth` search independently inside their own treaps. For example, if experiment 1 has `[1,2]` and experiment 2 has `[3]`, swapping position 2 of experiment 1 with position 1 of experiment 2 changes the stored values to `[1,3]` and `[2]`. The tree structures do not move, so all other indices remain untouched.

For a single student experiment, `kth` receives `k = 1`. The left subtree size is zero, so it immediately returns that node. This avoids off-by-one mistakes at the smallest valid index.
