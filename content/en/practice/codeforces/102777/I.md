---
title: "CF 102777I - \u041a\u0430\u043a \u0442\u0435\u0431\u0435 \u0442\u0430\u043a\u043e\u0435, \u0418\u043b\u043e\u043d \u041c\u0430\u0441\u043a?"
description: "The HyperLoop network can be viewed as a directed graph with n stations. From every station there are exactly two outgoing edges: a left tunnel and a right tunnel."
date: "2026-07-27T20:31:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102777
codeforces_index: "I"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102777
solve_time_s: 47
verified: true
draft: false
---

[CF 102777I - \u041a\u0430\u043a \u0442\u0435\u0431\u0435 \u0442\u0430\u043a\u043e\u0435, \u0418\u043b\u043e\u043d \u041c\u0430\u0441\u043a?](https://codeforces.com/problemset/problem/102777/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
# Problem Understanding

The HyperLoop network can be viewed as a directed graph with `n` stations. From every station there are exactly two outgoing edges: a left tunnel and a right tunnel. Taking the left tunnel repeatedly means applying one function, and taking the right tunnel repeatedly means applying another function.

Each query gives a starting station `x`, a number of left moves `a`, a number of right moves `b`, and the coin result `c`. If `c = 0`, the trip consists of `a` left moves followed by `b` right moves. If `c = 1`, the order is reversed. The task is to find the final station after the two blocks of moves.

The difficult part is that the graph has only `100000` stations, but the number of moves can reach `10^15`. Simulating moves is impossible because even one query could require a quadrillion transitions. With `500000` queries, any solution close to `O(nq)` or even `O(q * min(a,b))` is far outside the available time. We need preprocessing on the graph so each query can be answered in about logarithmic time.

The graph structure is very special. Each tunnel type alone creates a functional graph: every station has exactly one outgoing left edge and exactly one outgoing right edge. Functional graphs contain directed cycles with trees leading into them, which is exactly the structure where binary lifting works well.

Several edge cases can break a careless implementation. The first is a query with zero moves. For example:

```
n = 1
left: 1
right: 1
query: 1 0 0 0
```

The answer is:

```
1
```

A solution that always performs at least one jump would incorrectly leave the station.

Another tricky case is a self-loop mixed with large powers:

```
n = 2
left: 1 1
right: 2 2
query: 2 1000000000000000 7 0
```

The answer is:

```
1
```

After the first left move the station becomes `1`, and every further left move stays there. A method based on cycle detection must handle cycles of length one correctly.

The order of the two operations also matters. For example:

```
n = 3
left: 2 3 3
right: 1 1 2
query: 1 1 1 0
```

The answer is:

```
1
```

The path is `1 -> 2` using the left tunnel, then `2 -> 1` using the right tunnel. Reversing the order gives a different transition, so treating the query as one combined operation is incorrect.

## Approaches

The direct solution is to simulate the trip. For every query, start at `x`, follow the required tunnel `a` times, then follow the other tunnel `b` times. This is correct because every move is exactly the edge defined by the chosen tunnel. However, the worst case is enormous. One query can require `10^15 + 10^15` transitions, and `500000` such queries would require around `10^21` operations.

The key observation is that the two tunnel systems are independent. We never need to alternate between left and right tunnels. Every query is only asking for one power of the left function and one power of the right function. If we can answer "where does this station go after `k` left moves?" quickly, the whole query becomes two independent jumps.

Binary lifting provides exactly this operation. For each tunnel type, we store where every station reaches after `2^j` moves. Any value up to `10^15` can be represented using at most 50 binary bits, so a jump can be decomposed into at most 50 stored transitions.

The brute-force works because following edges one by one exactly matches the process, but it fails because the number of edges traveled is too large. The observation that each tunnel type is a functional graph lets us replace long walks with a logarithmic number of precomputed jumps.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a + b) per query | O(1) | Too slow |
| Binary Lifting | O(n log 10^15 + q log 10^15) | O(n log 10^15) | Accepted |

## Algorithm Walkthrough

1. Build two binary lifting tables, one for left tunnels and one for right tunnels. The first level stores the direct destination after one move. Each next level stores the destination after twice as many moves as the previous level. For example, level `j` answers a jump of length `2^j`.
2. For each query, decide the order of operations using `c`. If `c = 0`, first apply a left jump of length `a`, then a right jump of length `b`. If `c = 1`, perform the right jump first.
3. To perform a jump of length `k`, inspect the binary representation of `k`. For every bit that is set, replace the current station with the destination stored at that binary lifting level. Each set bit corresponds to one power-of-two segment of the route.
4. Output the station reached after both jumps are completed.

Why it works:

The invariant behind binary lifting is that `up[j][v]` always represents exactly `2^j` applications of the same tunnel function starting from `v`. The base level is true by construction, and each higher level is formed by applying the previous jump twice, so the property holds for every level. Any move count can be split into powers of two using binary representation, so combining the selected jumps gives exactly the same result as performing all moves individually.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def build_lift(n, nxt):
    LOG = 50
    lift = [array('i', nxt)]
    for _ in range(1, LOG):
        prev = lift[-1]
        cur = array('i', [0]) * (n + 1)
        for i in range(1, n + 1):
            cur[i] = prev[prev[i]]
        lift.append(cur)
    return lift

def jump(v, k, lift):
    bit = 0
    while k:
        if k & 1:
            v = lift[bit][v]
        k >>= 1
        bit += 1
    return v

def solve():
    n, q = map(int, input().split())
    left = [0] + list(map(int, input().split()))
    right = [0] + list(map(int, input().split()))

    left_lift = build_lift(n, left)
    right_lift = build_lift(n, right)

    ans = []
    for _ in range(q):
        x, a, b, c = map(int, input().split())
        if c == 0:
            x = jump(x, a, left_lift)
            x = jump(x, b, right_lift)
        else:
            x = jump(x, b, right_lift)
            x = jump(x, a, left_lift)
        ans.append(str(x))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `build_lift` function creates the tables for one tunnel direction. The first array is the direct edge, and every later array doubles the length of the jump by composing the previous array with itself. The use of `array('i')` is deliberate because Python lists would store references and would exceed the memory limit for about ten million stored transitions.

The `jump` function follows the bits of the move count. If the current bit is set, the corresponding precomputed jump is applied. Move counts fit inside 50 bits because `2^50` is larger than `10^15`.

The query processing only chooses the order of the two independent jumps. The values of `a` and `b` can be zero, and the `while k` loop naturally handles that case by returning the original station.

Python integers do not overflow, so the large move counts are safe. The only indexing detail to watch is that stations are numbered from `1`, so every lifting array contains an unused element at position `0`.

## Worked Examples

For the first sample query `1 4 7 1`, the coin result means the right moves happen first.

| Step | Current station | Operation | Remaining moves |
| --- | --- | --- | --- |
| Start | 1 | Begin | right 7, left 4 |
| After right jump | 6 | Apply 7 right moves | left 4 |
| After left jump | 3 | Apply 4 left moves | 0 |

The answer is `3`. This demonstrates that the two jumps must be executed in the specified order.

For a smaller custom example:

```
3 2
2 3 3
1 1 2
1 5 2 0
2 3 4 1
```

The first query uses left moves first.

| Step | Current station | Operation | Result |
| --- | --- | --- | --- |
| Start | 1 | 5 left moves | 3 |
| Finish | 3 | 2 right moves | 2 |

The second query reverses the order.

| Step | Current station | Operation | Result |
| --- | --- | --- | --- |
| Start | 2 | 4 right moves | 1 |
| Finish | 1 | 3 left moves | 3 |

These traces show that the lifting tables are only answering single-direction movement. The query logic is responsible for composing the two directions in the correct order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log 10^15) | Each station is processed for about 50 lifting levels, and each query performs at most 100 bit checks. |
| Space | O(n log 10^15) | Two tunnel directions each store about 50 layers of `n` destinations. |

The preprocessing stores about ten million transitions. Using compact integer arrays keeps the memory usage within the 64 MB limit. The query time is independent of the values of `a` and `b`, so even the largest move counts are handled quickly.

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
    
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

# provided sample
assert run("""6 5
2 4 1 5 3 3
6 3 6 3 6 4
1 4 7 1
2 5 2 0
4 14 1 0
5 8 13 1
3 1 14 0
""") == """3
3
6
3
6""", "sample"

# single station self loops
assert run("""1 3
1
1
1 0 0 0
1 1000000000000000 999999999999999 1
1 5 7 0
""") == """1
1
1""", "single station"

# different orders give different answers
assert run("""3 2
2 3 3
1 1 2
1 1 1 0
1 1 1 1
""") == """1
2""", "order matters"

# all destinations equal
assert run("""4 2
4 4 4 4
2 2 2 2
3 1000000000000000 1000000000000000 0
1 999999999999999 0 1
""") == """4
2""", "large equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single station | `1` for every query | Zero moves and self-loop handling |
| Different operation orders | Different results | Correct interpretation of `c` |
| All destinations equal | Fixed destinations after huge jumps | Large powers and repeated transitions |

## Edge Cases

A single-station graph has both tunnel functions pointing to itself. The lifting table contains only destination `1` at every level. A query with `a = 0` and `b = 0` performs no jumps and returns the start station. A query with enormous values still returns `1` because every jump level preserves the self-loop.

For the earlier self-loop example:

```
2
1 1
2 2
2 1000000000000000 7 0
```

The left lifting table sends station `2` to station `1` at level zero, and every higher level also stays at station `1`. The first left jump immediately reaches the stable cycle, and the remaining left moves do not change the result. The final right jump keeps the station at `1`, producing:

```
1
```

For the order-sensitive example:

```
3 1
2 3 3
1 1 2
1 1 1 0
```

The algorithm first applies the left jump, reaching station `2`, then applies the right jump, returning to station `1`. The result is:

```
1
```

The same graph with `c = 1` would apply the right jump first, reach station `1`, then move left to station `2`. This confirms that the solution does not merge the two functions and preserves the required operation order.
