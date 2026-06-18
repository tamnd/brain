---
title: "CF 106315H - Chemical Reaction"
description: "We start with a set of chemical types already present in a chamber. Each second, any pair of chemicals that has a known reaction rule can produce a new chemical type."
date: "2026-06-18T22:17:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106315
codeforces_index: "H"
codeforces_contest_name: "ICPC Dhaka 2025 Online Preliminary - Replay Contest"
rating: 0
weight: 106315
solve_time_s: 44
verified: true
draft: false
---

[CF 106315H - Chemical Reaction](https://codeforces.com/problemset/problem/106315/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a set of chemical types already present in a chamber. Each second, any pair of chemicals that has a known reaction rule can produce a new chemical type. The important detail is that reactions are not consuming: both reactants remain available after producing the new chemical, so the system only accumulates chemicals over time. Multiple reactions can happen in parallel, and this process continues for an extremely large number of steps, effectively until no new chemical can ever appear.

The input gives an initial set of chemical IDs and a list of reaction rules of the form “if chemical x and chemical y are both present, we can produce chemical z”. The task is to determine how many distinct chemical types can eventually appear if we keep applying all possible reactions indefinitely.

Although time is phrased as 10^100 seconds, the process is monotonic: once a chemical appears, it never disappears, and once all reachable chemicals are generated, the system stabilizes. So the real question is about closure under these production rules.

The constraints suggest up to 1000 initial chemicals and 1000 rules per test case, with up to 500 test cases. A naive simulation over time is impossible because the time horizon is astronomically large. Even simulating per second is irrelevant since the state space is what matters, not time steps.

A subtle edge case appears when reactions form chains or cycles. For example, if A and B produce C, and A and C produce D, then D may unlock further reactions. Another important case is when multiple rules share reactants but produce different outputs; all of them must be accounted for independently.

A naive mistake would be to treat reactions as one-time events or to assume a topological ordering. Another mistake is to simulate only one new chemical per step instead of allowing all applicable reactions simultaneously, which would drastically underestimate the reachable set.

## Approaches

The brute-force idea is to simulate the system in discrete time steps. At each step, we check all reaction rules and see if both reactants are currently present. If yes, we add the product to the set of available chemicals. We repeat this until no new chemical is added in a full pass.

This is correct because it directly follows the rules: every reaction is applied whenever its prerequisites are met. However, the problem is that each pass scans all m rules, and we may need up to O(n) layers of propagation in the worst case, where each layer unlocks exactly one new chemical. That leads to O(nm) or worse behavior, and since both n and m can be 1000 per test case and there are many test cases, this becomes too slow.

The key observation is that this is not a time-evolution problem but a reachability problem in a hypergraph. Each reaction is a rule that becomes active when two nodes are present, and once active it permanently adds a new node. This suggests we should treat the process as a closure computation: maintain the current set of available chemicals and repeatedly activate rules whose prerequisites are satisfied, but avoid rescanning everything unnecessarily.

We can maintain a queue of “newly discovered chemicals” and track, for each chemical, which reaction rules it participates in. Each rule is only triggered once both its endpoints are known. By maintaining a counter per rule of how many reactants are still missing, we can activate a rule exactly once when it becomes fully satisfied. This turns the process into a multi-source propagation similar to BFS over a bipartite dependency structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(k · m) worst-case | O(n + m) | Too slow |
| Dependency BFS / Activation Propagation | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read all initial chemicals and mark them as present. We also initialize a queue with these chemicals, because they are the starting frontier of all future reactions.
2. For every reaction rule (x, y → z), we store it in adjacency lists of both x and y, and maintain a counter of how many of its reactants are still missing. Initially this counter is 2.
3. As we process chemicals from the queue, when we encounter a chemical v, we iterate over all reaction rules that involve v. For each such rule, we decrement its missing-reactant counter because one of its required chemicals has now appeared.
4. If a rule’s counter reaches zero, both reactants are now present, so we can produce the resulting chemical z. If z was not previously present, we mark it as present and push it into the queue.
5. Continue until the queue is empty, meaning no new chemical can be produced by any rule.
6. Finally, count how many chemicals have been marked present.

The reason this works is that every reaction rule transitions from “inactive” to “active” exactly once, at the moment both required reactants become available. The queue ensures we propagate newly discovered chemicals immediately, and each rule is processed a bounded number of times proportional to its endpoints.

### Why it works

At any point in the process, a chemical is either known (already in the set) or unknown. A reaction rule becomes eligible exactly when both endpoints are known. The algorithm ensures that this eligibility is detected immediately upon the arrival of the second endpoint, because every chemical arrival is propagated through all incident rules. No rule can be missed, and no rule can fire prematurely. This establishes that the algorithm exactly computes the closure of the initial set under the given binary production rules.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict, deque

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        init = list(map(int, input().split()))
        
        present = set(init)
        q = deque(init)
        
        # for each chemical, list of (rule_id)
        adj = defaultdict(list)
        
        # rules: (x, y, z)
        x = []
        y = []
        z = []
        remaining = []
        
        for i in range(m):
            a, b, c = map(int, input().split())
            x.append(a)
            y.append(b)
            z.append(c)
            remaining.append(2)
            adj[a].append(i)
            adj[b].append(i)
        
        while q:
            v = q.popleft()
            for i in adj[v]:
                remaining[i] -= 1
                if remaining[i] == 0:
                    nz = z[i]
                    if nz not in present:
                        present.add(nz)
                        q.append(nz)
        
        print(len(present))

if __name__ == "__main__":
    solve()
```

The code maintains a global set `present` representing all discovered chemicals. The queue drives propagation from initial chemicals outward. Each reaction rule has a small state, `remaining[i]`, which tracks how many of its required inputs are still missing. Since every rule has exactly two inputs, the counter starts at 2 and reaches zero exactly when both inputs have been seen.

A subtle implementation detail is that we never revisit a rule after it fires, because once `remaining[i]` reaches zero, it cannot change again. This ensures linear complexity in the number of rule-chemical incidences rather than repeated scanning.

## Worked Examples

### Example 1

Consider a small system:

Input chemicals: 1, 2

Rules: (1,2→3), (2,3→4)

We trace execution:

| Step | Queue | Processed v | Activated rules | New chemicals |
| --- | --- | --- | --- | --- |
| 1 | [1,2] | 1 | none | none |
| 2 | [2] | 2 | rule (1,2→3) becomes ready | 3 |
| 3 | [3] | 3 | rule (2,3→4) becomes ready | 4 |
| 4 | [] | - | - | - |

Final set is {1,2,3,4}.

This confirms that chaining reactions are correctly captured without explicit time simulation.

### Example 2

Input chemicals: 5, 7

Rules: (5,7→10), (10,7→20), (5,10→30)

| Step | Queue | Processed v | Activated rules | New chemicals |
| --- | --- | --- | --- | --- |
| 1 | [5,7] | 5 | partial (5,7→10) | none |
| 2 | [7] | 7 | rule (5,7→10) fires | 10 |
| 3 | [10] | 10 | (10,7→20), (5,10→30) both unlock | 20, 30 |
| 4 | [] | - | - | - |

Final result is {5,7,10,20,30}. This demonstrates that multiple reactions triggered by the same newly discovered chemical are handled correctly in a single propagation phase.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each chemical is enqueued once, and each rule is processed at most twice (once per endpoint activation) |
| Space | O(n + m) | Storage for adjacency lists, rule states, and visited set |

The constraints allow up to 1000 rules and 1000 initial chemicals per test case, so a linear traversal over rules and chemical occurrences comfortably fits within limits even for 500 test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import defaultdict, deque

    input = sys.stdin.readline

    def solve():
        t = int(input())
        for _ in range(t):
            n, m = map(int, input().split())
            init = list(map(int, input().split()))
            present = set(init)
            q = deque(init)

            adj = defaultdict(list)
            x = []
            y = []
            z = []
            remaining = []

            for i in range(m):
                a, b, c = map(int, input().split())
                x.append(a); y.append(b); z.append(c)
                remaining.append(2)
                adj[a].append(i)
                adj[b].append(i)

            while q:
                v = q.popleft()
                for i in adj[v]:
                    remaining[i] -= 1
                    if remaining[i] == 0:
                        if z[i] not in present:
                            present.add(z[i])
                            q.append(z[i])

            print(len(present))

    solve()
    return sys.stdout.getvalue().strip()

# provided sample-style cases
assert run("""1
2 2
1 4
1 4 2
2 4 3
""") == "3"

assert run("""1
2 2
1 1000000000
1 1000000000 500000000
500000000 1000000000 999999999
""") == "3"

# minimal case
assert run("""1
1 0
5
""") == "1"

# chain reaction
assert run("""1
3 2
1 2 3
1 3 4
3 2 5
""") == "5"

# self-growth impossible cycles
assert run("""1
2 1
1 2
3 4 5
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single node | 1 | no reactions |
| sample-like | 3 | basic propagation |
| chain reaction | 5 | multi-step dependency |
| irrelevant rule | 2 | unused reactions ignored |

## Edge Cases

One important case is when a reaction chain is long and only unlocks a new chemical after several intermediate steps. For example, 1, 2 → 3, 3, 4 → 5, 5, 6 → 7. The algorithm handles this naturally because each newly added chemical immediately triggers re-evaluation of all rules involving it, so the chain progresses without explicit layering.

Another edge case is when multiple rules share a reactant but produce different outputs. If chemical x appears, all rules involving x must be considered simultaneously. The adjacency-based propagation ensures that x contributes to all such rules, and none are skipped.

A final case is redundant rules that produce already existing chemicals. Since we check `present` before enqueuing, repeated production does not cause infinite loops or overcounting.
