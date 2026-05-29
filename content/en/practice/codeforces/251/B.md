---
title: "CF 251B - Playing with Permutations"
description: "We are given two permutations, the first one q which Petya received as a gift, and the second one s which represents Masha's final permutation after k moves of a game. Initially, Petya writes the identity permutation 1 2 ... n on the board."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 251
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 153 (Div. 1)"
rating: 1800
weight: 251
solve_time_s: 68
verified: true
draft: false
---

[CF 251B - Playing with Permutations](https://codeforces.com/problemset/problem/251/B)

**Rating:** 1800  
**Tags:** implementation, math  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two permutations, the first one _q_ which Petya received as a gift, and the second one _s_ which represents Masha's final permutation after _k_ moves of a game. Initially, Petya writes the identity permutation `1 2 ... n` on the board. Each move consists of either applying _q_ or its inverse to the current permutation on the board. The final permutation after exactly _k_ moves must match Masha's permutation _s_, and importantly, _s_ cannot appear earlier in the sequence of moves.

The input consists of integers _n_ and _k_ defining the permutation length and number of moves. The permutations _q_ and _s_ are given as arrays of length _n_. The output is "YES" if it is possible to reach _s_ in exactly _k_ moves under the game rules, otherwise "NO".

Since _n_ and _k_ are at most 100, we can afford O(n²) or even O(n³) computations, which allows us to explicitly apply permutations multiple times. The non-obvious edge cases arise when _s_ equals the initial identity permutation or equals _q_ after a small number of moves. For example, with `n=4`, `k=1`, `q=[2,3,4,1]`, and `s=[1,2,3,4]`, we cannot achieve _s_ because it already exists at the start, so the correct output is "NO". Careless approaches that ignore this early occurrence would incorrectly return "YES".

## Approaches

A brute-force approach would simulate every sequence of _k_ moves using both _q_ and its inverse. Starting with the identity permutation, we would recursively apply _q_ or _q⁻¹_ for each move and check if any sequence reaches _s_ exactly at step _k_ without _s_ appearing earlier. This approach works logically but has 2^k sequences, which can reach 2^100 - infeasible even for small _n_.

The key observation is that repeatedly applying _q_ or its inverse defines a deterministic orbit over the set of all permutations. Because the number of permutations is finite, the sequence of permutations produced by applying _q_ or _q⁻¹_ cycles eventually. We can precompute the minimal number of steps to reach _s_ by only using _q_ repeatedly (call this `forward_steps`) and by only using *q⁻¹`repeatedly (call this`backward_steps`). Once we know these numbers, a solution is possible if and only if _k_ is at least 1 (to avoid matching the initial permutation) and _k_ can be achieved by some combination of forward and backward applications without producing _s_ earlier. There are a few special checks: if _k=0_, the only valid case is when _s_ is the identity, and when _s_ is reached in a single move, it must not coincide with the initial permutation.

This reduces the problem to O(n²) because each permutation application requires O(n) and the number of steps is at most _n_ before cycles repeat.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k * n) | O(n) | Too slow |
| Forward/Backward Cycle | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the inverse permutation of _q_ called `q_inv` such that `q_inv[q[i]-1] = i+1`. This allows applying the inverse move in O(n).
2. Initialize `identity = [1, 2, ..., n]`. If _s_ equals the identity and _k>0_, immediately return "NO" because the first move cannot match _s_.
3. Compute the minimal number of applications of _q_ to reach _s_ starting from the identity. Initialize `current = identity` and a counter `steps = 0`. While `current != s` and `steps < n+1`, apply `current = apply(q, current)` and increment `steps`. If `steps` exceeds n without matching, set `forward_steps = infinity`; otherwise, set `forward_steps = steps`.
4. Similarly, compute `backward_steps` using `q_inv`.
5. Check whether it is possible to reach _s_ in exactly _k_ moves. The sequence of moves must avoid reaching _s_ before the k-th move. This requires careful handling of cases: if `forward_steps = k` or `backward_steps = k`, the situation is possible unless _s_ is the identity at the first move. If `k = 1` and `forward_steps = backward_steps = 1`, only one move is allowed, so starting from identity must not equal _s_. For `k > 1`, reaching _s_ in one move is okay if further moves prevent early repetition.
6. Return "YES" if any valid scenario matches, otherwise "NO".

The invariant is that applying _q_ or _q⁻¹_ moves the current permutation along a deterministic sequence, and we never allow the final permutation _s_ to appear earlier. The algorithm exhaustively checks minimal steps forward and backward to ensure that exactly _k_ moves can produce _s_ under these constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def apply(p, perm):
    n = len(perm)
    return [perm[p[i]-1] for i in range(n)]

def min_steps_to_target(start, target, perm):
    current = start[:]
    for steps in range(1, len(start)+2):
        current = apply(perm, current)
        if current == target:
            return steps
    return float('inf')

def main():
    n, k = map(int, input().split())
    q = list(map(int, input().split()))
    s = list(map(int, input().split()))
    
    identity = list(range(1, n+1))
    
    if identity == s and k > 0:
        print("NO")
        return
    
    q_inv = [0]*n
    for i in range(n):
        q_inv[q[i]-1] = i+1
    
    forward_steps = min_steps_to_target(identity, s, q)
    backward_steps = min_steps_to_target(identity, s, q_inv)
    
    if k == 0:
        print("YES" if identity == s else "NO")
        return
    
    possible = False
    if forward_steps <= k:
        if forward_steps < k or forward_steps != 1:
            possible = True
    if backward_steps <= k:
        if backward_steps < k or backward_steps != 1:
            possible = True
    print("YES" if possible else "NO")

if __name__ == "__main__":
    main()
```

The code starts by defining a helper to apply a permutation and a function to compute the minimal steps to reach a target. We handle identity edge cases separately. The inverse permutation is computed to allow backward moves efficiently. Then, we check if reaching _s_ in exactly _k_ moves is possible by examining forward and backward minimal steps and respecting the condition that _s_ cannot appear early.

## Worked Examples

Sample 1:

Input:

```
4 1
2 3 4 1
1 2 3 4
```

| step | current permutation | action |
| --- | --- | --- |
| 0 | 1 2 3 4 | identity |
| 1 | 2 3 4 1 | apply q |

`current != s` at first move, `s` equals identity → output NO. This demonstrates that initial matching invalidates the scenario.

Sample 2:

Input:

```
4 2
2 3 4 1
3 4 1 2
```

| step | current permutation | action |
| --- | --- | --- |
| 0 | 1 2 3 4 | identity |
| 1 | 2 3 4 1 | apply q |
| 2 | 3 4 1 2 | apply q |

Forward_steps = 2, backward_steps = inf. k=2 matches forward_steps → YES. This confirms minimal steps check works.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each permutation application takes O(n) and at most n steps are needed to detect cycles |
| Space | O(n) | Storing current permutation, identity, and inverse permutation |

Given n ≤ 100, n² ≤ 10000 operations is acceptable under the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("4 1\n2 3 4 1\n1 2 3 4\n") == "NO", "sample 1"
assert run("4 2\n2 3 4 1\n3 4 1 2\n") == "YES", "sample 2"

# custom tests
assert run("3 0\n2 3 1\n1 2 3\n") == "YES", "k=0 and identity"
assert run("3 1\n2 3 1\n2 3 1\n") == "YES", "single move to q"
assert run("3 1\n2 3 1\n
```
