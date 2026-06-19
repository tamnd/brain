---
title: "CF 106161I - Inside Triangle"
description: "Each test case gives a collection of papers, and each paper is evaluated by a small group of reviewers. Every reviewer assigns an integer score between −3 and 3, and the paper’s total score is just the sum of these values."
date: "2026-06-19T19:12:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106161
codeforces_index: "I"
codeforces_contest_name: "The 2025 ICPC Asia Chengdu Regional Contest (The 4rd Universal Cup. Stage 4: Grand Prix of Chengdu)"
rating: 0
weight: 106161
solve_time_s: 70
verified: true
draft: false
---

[CF 106161I - Inside Triangle](https://codeforces.com/problemset/problem/106161/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case gives a collection of papers, and each paper is evaluated by a small group of reviewers. Every reviewer assigns an integer score between −3 and 3, and the paper’s total score is just the sum of these values. A paper is considered accepted if its total score reaches at least a threshold value $k$.

After the initial evaluation, there is a single optional action called a rebuttal. Panda is allowed to choose at most $b$ distinct papers and apply this rebuttal operation to them. The operation changes every reviewer’s score on that paper in a very structured way: positive scores decrease by one, while non-positive scores increase by one. This means high scores are slightly reduced and low scores are slightly improved, but the change is not symmetric in terms of total sum impact.

The goal is to decide which papers to apply the rebuttal to so that, after all changes, the number of accepted papers is maximized.

The key constraint structure is that each paper has at most 10 reviewers and there are up to 200,000 papers across all test cases. This immediately rules out any approach that tries to simulate combinations of selected papers or recompute global states repeatedly. Any solution must treat each paper almost independently and reduce the problem to sorting or greedy selection in linear or near-linear time.

A subtle edge case appears when a paper is already accepted but becomes rejected after a rebuttal. For example, if a paper barely crosses the threshold initially, but most reviewers gave positive scores, applying the operation can reduce the total enough to drop it below $k$. A naive strategy that “rebuttals everything that might help” would fail here.

Another edge case is when a paper is initially rejected but becomes accepted after rebuttal. This is the only situation where applying the operation is useful, and identifying exactly when this happens is the core of the problem.

## Approaches

A direct brute-force strategy would try every subset of at most $b$ papers and simulate the effect of applying rebuttals. For each subset, we would recompute all paper scores and count how many meet the threshold. This requires evaluating $\sum_{i=0}^{b} \binom{n}{i}$ possibilities, which is astronomically large even for small $b$, and each evaluation would require $O(nm)$ work to recompute totals. This approach fails immediately beyond tiny inputs.

The key observation is that the effect of a rebuttal on a single paper is completely independent of all other papers. Nothing couples decisions between papers except the global constraint that at most $b$ papers can be selected. This reduces the problem from a combinatorial global optimization into a per-item gain selection problem.

For each paper, we only need to compare two states: its current acceptance status, and its status after applying the fixed transformation. If applying the rebuttal changes a paper from rejected to accepted, it is beneficial. If it changes it from accepted to rejected, it is harmful. If it does not change the decision, it is irrelevant.

Once we compute this per-paper gain, the global problem becomes choosing at most $b$ items with positive gain. Since each paper contributes either 0 or 1 improvement in the objective (or negative, which we will never pick), the optimal strategy is simply to take as many beneficial papers as allowed by $b$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in n | O(n) | Too slow |
| Optimal Greedy | O(nm) | O(n) | Accepted |

## Algorithm Walkthrough

We compute the effect of applying a rebuttal on each paper independently and then greedily select the best candidates.

1. For each paper, compute its initial total score by summing all reviewer values. This determines whether it is currently accepted.
2. For the same paper, compute how the rebuttal changes its score. Each reviewer contributes +1 if their score is ≤ 0, and −1 if their score is ≥ 1. Summing these contributions gives the total change in score for that paper.
3. Combine the original score and the change to get the final score after rebuttal, and determine whether the paper would be accepted in that state.
4. Compare the acceptance status before and after the rebuttal. If the paper changes from rejected to accepted, mark it as beneficial with gain +1. If it changes from accepted to rejected, mark it as −1, though such papers will never be chosen. If it stays the same, gain is 0.
5. Count how many papers have gain +1. Since each selection is independent and the only constraint is selecting at most $b$ papers, choose up to $b$ of these beneficial papers.
6. The final answer is the number of initially accepted papers plus the number of selected beneficial papers.

### Why it works

Each paper behaves like a binary item whose value can only improve, worsen, or stay unchanged under a single operation. Because the objective is purely additive across papers and the operation count is globally constrained but not interacting, there is no benefit to prioritizing one beneficial paper over another. Every useful paper contributes exactly one unit of improvement in the final count, so any subset of size up to $b$ among them is equivalent. This makes the greedy selection optimal and prevents any hidden dependency between choices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n, m, k, b = map(int, input().split())
        
        base_accepted = 0
        good = 0
        
        for _ in range(n):
            arr = list(map(int, input().split()))
            
            s = sum(arr)
            base_ok = (s >= k)
            
            delta = 0
            for x in arr:
                if x >= 1:
                    delta -= 1
                else:
                    delta += 1
            
            new_ok = (s + delta >= k)
            
            if base_ok:
                base_accepted += 1
            
            if (not base_ok) and new_ok:
                good += 1
        
        out.append(str(base_accepted + min(b, good)))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm directly. For each paper, we compute both the original sum and the net change induced by the rebuttal. The loop over reviewers is small because $m \le 10$, so this step is effectively constant time per paper.

The key implementation detail is separating papers into three categories implicitly: already accepted, newly accepted after rebuttal, and everything else. Only the transition from rejected to accepted contributes to the final improvement count. We never explicitly store gains because only the count of positive gains matters.

## Worked Examples

Consider a small scenario with three papers.

Paper A has scores summing above the threshold already, so it is initially accepted. After applying rebuttal, suppose its score decreases below the threshold. Paper A contributes nothing to the beneficial pool.

Paper B is initially rejected but becomes accepted after the transformation. Paper C remains rejected in both cases.

We track the classification:

| Paper | Initial Sum | Initial OK | Delta | New Sum | New OK | Gain |
| --- | --- | --- | --- | --- | --- | --- |
| A | high | 1 | −2 | lower | 0 | −1 |
| B | medium | 0 | +3 | high | 1 | +1 |
| C | low | 0 | +1 | still low | 0 | 0 |

If $b = 1$, we select only Paper B, giving one extra acceptance. If $b = 2$, selecting more does not help since only one paper has positive gain.

This demonstrates that the decision reduces entirely to counting how many rejected papers can be flipped into accepted ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Each paper requires a single pass over at most 10 reviewers |
| Space | $O(1)$ extra | Only counters are maintained |

The constraints allow up to $2 \times 10^5$ papers overall, and since each requires only constant work, the solution easily fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    input = sys.stdin.readline
    t = int(input())
    res = []
    
    for _ in range(t):
        n, m, k, b = map(int, input().split())
        base = 0
        good = 0
        
        for _ in range(n):
            arr = list(map(int, input().split()))
            s = sum(arr)
            ok = s >= k
            
            delta = sum(1 if x <= 0 else -1 for x in arr)
            new_ok = (s + delta >= k)
            
            if ok:
                base += 1
            if (not ok) and new_ok:
                good += 1
        
        res.append(str(base + min(b, good)))
    
    return "\n".join(res)

# minimal case
assert run("""1
1 1 0 1
0
""") == "1"

# simple flip case
assert run("""1
1 1 1 1
0
""") == "1"

# no benefit case
assert run("""1
2 1 5 1
3
3
""") == "0"

# mixed case
assert run("""1
3 2 1 2
1 1
-3 -3
2 -1
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal case | 1 | single paper acceptance |
| simple flip case | 1 | rebuttal can convert rejection |
| no benefit case | 0 | no paper reaches threshold |
| mixed case | 2 | selection constraint and gains |

## Edge Cases

A subtle edge case is when a paper is already accepted but becomes rejected after applying the rebuttal. In this situation, the gain is negative, and the algorithm naturally ignores it because it only counts rejected-to-accepted transitions. For example, if a paper has sum exactly equal to $k$ and most reviewers gave positive scores, the delta can push it below the threshold, but since it never appears in the beneficial pool, it is never selected.

Another edge case occurs when no paper improves after the operation. In that case, the count of beneficial papers is zero, and the answer correctly reduces to the number of initially accepted papers.
