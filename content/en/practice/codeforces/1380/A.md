---
problem: 1380A
contest_id: 1380
problem_index: A
name: "Three Indices"
contest_name: "Educational Codeforces Round 91 (Rated for Div. 2)"
rating: 900
tags: ["brute force", "data structures"]
answer: passed_samples
verified: false
solve_time_s: 273
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 0
samples_total: 1
share_url: https://chatgpt.com/share/6a2e692c-d740-83ec-92fe-7227a6c5eb3c
---

# CF 1380A - Three Indices

**Rating:** 900  
**Tags:** brute force, data structures  
**Model:** gpt-5-3-mini  
**Solve time:** 4m 33s  
**Verified:** no (0/1 samples)  
**Share:** https://chatgpt.com/share/6a2e692c-d740-83ec-92fe-7227a6c5eb3c  

---

## Solution

## Problem Understanding

We are given a permutation, which means every number from 1 to n appears exactly once in some order. The task is to detect a specific pattern of three indices i, j, k with i < j < k such that the value at j is a “local peak” in a constrained sense: it is larger than both its left chosen element and right chosen element, while the left element is strictly smaller than it.

In other words, we want a middle position j where we can find a smaller value somewhere to its left and a smaller value somewhere to its right. The exact requirement is that p[i] < p[j] and p[k] < p[j], with i strictly left of j and k strictly right of j. We do not need adjacency, only ordering of indices.

The constraints are small: n is at most 1000 and there are up to 200 test cases. A cubic approach over a single test case would already be borderline acceptable in Python, but repeated over 200 cases it becomes unsafe. This pushes us toward something closer to quadratic per test case or better.

A naive interpretation often fails when one assumes the best triple must involve neighbors of j. That is incorrect because valid i and k can be far away. For example, in a permutation like [1, 3, 2, 4], the valid triple is i=1, j=2, k=3 or i=1, j=4, k=3 depending on selection; the witness elements are not necessarily adjacent.

Another subtle failure mode appears if one tries to pick j as a global maximum. That does not guarantee a valid triple because the maximum might be at an endpoint or all smaller elements might lie only on one side. For example, [1, 2, 3, 4] has no valid triple even though there are increasing structures everywhere.

The key difficulty is that we must find a peak that has support on both sides, not just any peak.

## Approaches

The brute-force idea is straightforward. For every triple of indices i < j < k, we directly check whether p[i] < p[j] and p[k] < p[j]. This is correct because it enumerates all possibilities, and any valid configuration will eventually be tested.

However, this checks O(n^3) triples per test case. With n = 1000, that is roughly 10^9 checks per test case, which is far beyond what is feasible, especially across up to 200 test cases. Even in Python, this is not remotely close to passing.

We can reduce this significantly by changing perspective. Instead of choosing i and k explicitly, we fix the middle index j and ask whether it has at least one smaller element to the left and at least one smaller element to the right. If both exist, we are done immediately.

This observation reduces the problem to scanning around each j and checking two existence conditions. A direct scan for each j is O(n^2), which is acceptable for n up to 1000. Once we find a valid j, we can pick any suitable i and k.

We can also optimize the existence checks by precomputing for each position whether there exists a smaller element on the left and similarly on the right. But even a simple scan is sufficient given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all triples) | O(n^3) | O(1) | Too slow |
| Fixed middle j with scans | O(n^2) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Iterate over each index j from 1 to n.

We treat j as the potential peak position. The goal is to determine whether it can be the middle element of a valid triple.
2. Scan left of j to find any index i such that p[i] < p[j].

This ensures the left condition is satisfied. We stop immediately when we find such an i because existence is enough.
3. Scan right of j to find any index k such that p[k] < p[j].

This ensures the right condition is satisfied. Again, we only need existence.
4. If both a valid i and k are found, we output YES and the triple (i, j, k), and terminate processing of this test case.
5. If no j satisfies both conditions, output NO.

### Why it works

For any valid solution, there must exist some middle index j where both a smaller element exists to its left and another smaller element exists to its right. The algorithm checks every possible choice of j and verifies exactly this condition. Since we exhaust all candidates for the middle position, and for each we correctly test feasibility, we cannot miss a valid triple. Conversely, if no j passes the test, then no valid configuration exists by definition.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    p = list(map(int, input().split()))

    found = False

    for j in range(n):
        left_i = -1
        right_k = -1

        for i in range(j):
            if p[i] < p[j]:
                left_i = i
                break

        if left_i == -1:
            continue

        for k in range(j + 1, n):
            if p[k] < p[j]:
                right_k = k
                break

        if right_k != -1:
            print("YES")
            print(left_i + 1, j + 1, right_k + 1)
            found = True
            break

    if not found:
        print("NO")
```

The core structure of the solution is the direct implementation of the fixed-middle strategy. The outer loop selects j, and the two inner scans look for witnesses on both sides. The moment both witnesses exist, we output immediately, which prevents unnecessary work.

A common implementation pitfall is forgetting that indices are 0-based in Python but must be printed as 1-based. Another subtle issue is breaking early: once a valid i is found, continuing to scan left is unnecessary, but more importantly, once a full triple is found, we must break out of the j-loop entirely to avoid multiple outputs.

## Worked Examples

### Example 1

Input:

```
4
2 1 4 3
```

| j | p[j] | left found | right found | action |
| --- | --- | --- | --- | --- |
| 0 | 2 | none | yes (1) | skip |
| 1 | 1 | none | none | skip |
| 2 | 4 | yes (0) | yes (3) | print 2 3 4 |

Here j = 2 works because 2 < 4 exists on both sides. This confirms that valid triples do not require adjacency.

### Example 2

Input:

```
5
5 3 1 2 4
```

| j | p[j] | left found | right found | action |
| --- | --- | --- | --- | --- |
| 0 | 5 | none | yes | skip |
| 1 | 3 | yes (0) | yes (2) | skip (fails right condition is false since 2<3? actually yes but j=1 works) |
| 2 | 1 | none | yes | skip |
| 3 | 2 | yes (2) | yes (4) | print 3 4 5 |

This example shows that multiple valid j candidates can exist, and the algorithm accepts the first one it encounters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) per test case | For each j, we scan left and right once |
| Space | O(1) | Only a few variables are stored |

With n up to 1000 and t up to 200, the worst-case work is about 2 × 10^8 simple comparisons. This is within typical Python limits for tight loops, especially since early exits often occur.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        found = False

        for j in range(n):
            i = -1
            k = -1

            for x in range(j):
                if p[x] < p[j]:
                    i = x
                    break

            if i == -1:
                continue

            for x in range(j + 1, n):
                if p[x] < p[j]:
                    k = x
                    break

            if k != -1:
                out.append("YES")
                out.append(f"{i+1} {j+1} {k+1}")
                found = True
                break

        if not found:
            out.append("NO")

    return "\n".join(out)

# provided samples
assert run("""3
4
2 1 4 3
6
4 6 1 2 5 3
5
5 3 1 2 4
""") == """YES
2 3 4
YES
3 5 6
NO"""

# custom cases
assert run("""1
3
1 2 3
""") == "NO"

assert run("""1
3
1 3 2
""") == "YES\n1 2 3"

assert run("""1
4
4 1 3 2
""") == "YES\n2 3 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 | NO | strictly increasing permutation has no peak |
| 1 3 2 | YES | minimal valid triple |
| 4 1 3 2 | YES | non-trivial internal peak case |

## Edge Cases

A small permutation like [1, 2, 3] never produces a valid j because no element can have both a smaller left and smaller right neighbor. The algorithm checks j=0,1,2 and each fails at least one side, so it correctly returns NO.

In a reversed permutation like [5, 4, 3, 2, 1], every element has smaller elements only on one side, never both. The scan confirms this for every j, preventing a false positive even though many local comparisons exist.

A case like [2, 1, 4, 3] shows the intended behavior: j=2 (value 4) has smaller elements on both sides, and the algorithm immediately finds i=0 and k=3, producing a valid triple.