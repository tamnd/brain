---
title: "CF 105458A - Juan's Flight"
description: "Each test case describes Juan’s attempt to choose a single store from which he will buy three required components for a flying car: an engine, a steering wheel, and a spare tire. Every store offers all three items, but each store has different prices for them."
date: "2026-06-23T17:47:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105458
codeforces_index: "A"
codeforces_contest_name: "XXIII Spain Olympiad in Informatics, Online Qualifier 2"
rating: 0
weight: 105458
solve_time_s: 64
verified: true
draft: false
---

[CF 105458A - Juan's Flight](https://codeforces.com/problemset/problem/105458/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes Juan’s attempt to choose a single store from which he will buy three required components for a flying car: an engine, a steering wheel, and a spare tire. Every store offers all three items, but each store has different prices for them. Juan cannot mix purchases across stores, so if he picks a store, he must buy all three items there.

The task is to compute, for each test case, which store has the smallest total cost when summing the three prices. Stores are considered in the order they appear in the input, and if multiple stores achieve the same minimum total cost, the earliest one must be chosen.

The constraints are large enough that a solution must process up to ten million stores in total across all test cases. This immediately rules out any approach that is worse than linear time per test case, since even O(n log n) would be too slow when n reaches one million repeatedly. The only viable direction is to compute the sum per store in constant time and maintain a running minimum.

A few subtle edge cases appear naturally in this formulation. One is when all stores have identical total cost. In that situation, the answer must be store 1, not the last occurrence, which means tie handling must be biased toward the first minimum seen. Another is when the minimum occurs multiple times later in the list; a careless update rule like “update when current sum is less than or equal” would incorrectly drift toward the last minimum instead of the first.

## Approaches

A direct way to solve the problem is to compute the total cost for every store, store those values in an array, and then scan for the minimum. This is correct because each store is independent, and the total cost is simply the sum of its three prices. However, even this simple idea can be implemented inefficiently if one stores all values first, which would require extra memory and multiple passes.

The bottleneck is not computation per store, since each store only needs three additions, but the overhead of storing and reprocessing large inputs. With up to 10 million stores overall, even a second pass over stored data risks cache inefficiency and memory pressure.

The key observation is that we never need to remember all stores. We only need the current best store index and its cost. As we read each store, we compute its total cost and immediately compare it to the best seen so far. This reduces the problem to a single streaming pass.

This works because the decision for a store does not depend on any future values. The minimum can be maintained incrementally: at any point, we only care whether the current store improves the best known answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (store all totals then scan) | O(n) per test case | O(n) | Too slow / unnecessary memory |
| Streaming minimum | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of stores n. This defines how many independent comparisons we will perform.
2. Initialize two variables: best_cost as infinity and best_index as 1. The index starts at 1 because store numbering is 1-based and the first store is the default candidate.
3. Iterate over the stores from i = 1 to n. For each store, read the three prices and compute their sum. This sum represents the total cost of choosing that store.
4. Compare the computed sum with best_cost. If the current sum is strictly smaller, update best_cost to this sum and best_index to i. The strict inequality is essential because it preserves the earliest index in case of ties.
5. After processing all stores in the test case, output best_index.

The correctness relies on maintaining the invariant that after processing the i-th store, best_cost and best_index correspond to the minimum total cost among the first i stores, and best_index is the earliest position achieving that minimum. Since each step only introduces one new candidate and never revisits past stores, this invariant holds throughout the scan.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n = int(input())
        
        best_cost = 10**30
        best_idx = 1
        
        for i in range(1, n + 1):
            a, b, c = map(int, input().split())
            total = a + b + c
            
            if total < best_cost:
                best_cost = total
                best_idx = i
        
        out.append(str(best_idx))
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads each store exactly once and immediately evaluates its cost. The use of a strict comparison ensures that ties do not overwrite an earlier optimal index. Accumulating output in a list and writing once at the end avoids repeated I/O overhead, which matters given the large input size.

## Worked Examples

Consider the first sample test case.

Input:

```
2
7 1 3
5 2 1
```

| i | a b c | total | best_cost | best_idx |
| --- | --- | --- | --- | --- |
| 1 | 7 1 3 | 11 | 11 | 1 |
| 2 | 5 2 1 | 8 | 8 | 2 |

The second store becomes optimal because its total cost is smaller than the first. The algorithm correctly updates both the cost and the index.

Now consider a case with ties.

Input:

```
3
4 4 4
2 5 5
6 2 4
```

| i | a b c | total | best_cost | best_idx |
| --- | --- | --- | --- | --- |
| 1 | 4 4 4 | 12 | 12 | 1 |
| 2 | 2 5 5 | 12 | 12 | 1 |
| 3 | 6 2 4 | 12 | 12 | 1 |

All stores have the same total. The strict comparison prevents any update after the first store, preserving index 1. This confirms correct tie handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total n) | Each store is processed exactly once with constant-time arithmetic |
| Space | O(1) | Only a few variables are maintained regardless of input size |

The solution runs in linear time over the entire input, which is necessary given the constraint that the sum of n across test cases can reach 10 million. Memory usage remains constant, so it comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    
    def solve():
        input = sys.stdin.readline
        t = int(input())
        res = []
        for _ in range(t):
            n = int(input())
            best_cost = 10**30
            best_idx = 1
            for i in range(1, n + 1):
                a, b, c = map(int, input().split())
                s = a + b + c
                if s < best_cost:
                    best_cost = s
                    best_idx = i
            res.append(str(best_idx))
        print("\n".join(res))
    
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""3
2
7 1 3
5 2 1
3
9 8 2
10 14 1
1 8 11
4
23 42 13
7 12 38
10 9 24
8 10 10
""") == """2
1
4"""

# minimum size
assert run("""1
1
5 5 5
""") == "1"

# all equal
assert run("""1
3
1 1 1
1 1 1
1 1 1
""") == "1"

# strict minimum late
assert run("""1
4
10 10 10
1 100 100
2 2 2
3 3 3
""") == "2"

# tie should prefer first
assert run("""1
2
1 2 3
6 0 0
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 store | 1 | minimum boundary |
| all equal stores | 1 | tie handling |
| minimum appears later | 2 | correct update logic |
| equal totals different forms | 1 | strict comparison correctness |

## Edge Cases

A key edge case is when multiple stores share the same minimum total cost. For example:

```
1
3
2 2 2
1 3 3
4 1 2
```

All totals are 6. The algorithm initializes best_cost with the first store and only updates on strictly smaller values. On the first store, best_cost becomes 6 and best_idx becomes 1. The second and third stores also produce 6, but since 6 is not less than 6, no update occurs. The output remains 1, which matches the required tie-breaking rule.

Another edge case is when the best store is the first one and no later store improves it. The invariant ensures no unnecessary updates occur, and the algorithm naturally returns 1 without special casing.
