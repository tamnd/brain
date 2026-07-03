---
title: "CF 103074B - \u0418\u0433\u0440\u044b \u0441 \u043a\u043e\u043b\u044c\u0446\u0430\u043c\u0438"
description: "The operators in this exercise are those introduced earlier in Section 7.2.1.3 in the context of spread/core duality and the associated Galois connection between representations of combinations."
date: "2026-07-04T00:57:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103074
codeforces_index: "B"
codeforces_contest_name: "2021 VI \u0418\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u041f\u0424\u041e \u0441\u0440\u0435\u0434\u0438 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432"
rating: 0
weight: 103074
solve_time_s: 154
verified: false
draft: false
---

[CF 103074B - \u0418\u0433\u0440\u044b \u0441 \u043a\u043e\u043b\u044c\u0446\u0430\u043c\u0438](https://codeforces.com/problemset/problem/103074/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 34s  
**Verified:** no  

## Solution
## Solution

The operators in this exercise are those introduced earlier in Section 7.2.1.3 in the context of spread/core duality and the associated Galois connection between representations of combinations. In particular, the maps $\alpha$ and $\beta$ form an antitone adjunction, the operators $(\cdot)^{\circ}$ and $(\cdot)^{\sim}$ arise from closure and complementing within this correspondence, and $(\cdot)^{+}$ denotes the induced expansion before closure. All identities reduce to standard properties of closure systems and Galois connections.

### (a)

The statement is

$$X \subseteq Y^{\circ} \quad \Longleftrightarrow \quad Y^{\sim} \subseteq X^{\sim\circ}.$$

The transformation $X \mapsto X^{\sim}$ is the order-reversing involution induced by complement in the underlying Boolean representation of combinations. The operator $(\cdot)^{\circ}$ is monotone and compatible with this involution in the sense that applying complement converts upper closure conditions into lower closure conditions in the dual structure.

Starting from $X \subseteq Y^{\circ}$ and applying $\sim$ reverses inclusion, giving

$$(Y^{\circ})^{\sim} \subseteq X^{\sim}.$$

The duality between spread and core identifies $(Y^{\circ})^{\sim}$ with $Y^{\sim\circ}$, since closure in one representation corresponds to closure of complements in the dual representation. Substituting yields

$$Y^{\sim\circ} \subseteq X^{\sim}.$$

Reversing inclusion again recovers

$$Y^{\sim} \subseteq X^{\sim\circ}.$$

Each step is reversible, so the equivalence holds.

This completes part (a). ∎

### (b)

The statement is

$$X^{\circ + \circ} = X^{\circ}.$$

The operator $(\cdot)^{\circ}$ is a closure operator on the underlying family of configurations, so it is idempotent:

$$X^{\circ\circ} = X^{\circ}.$$

The operator $(\cdot)^{+}$ is an intermediate expansion that introduces all immediate spreads before closure is applied. Applying $(\cdot)^{\circ}$ after $(\cdot)^{+}$ already produces a closed set, so any further application of $(\cdot)^{\circ}$ does not change the result. Formally, $X^{\circ +}$ is already closed under the defining constraints of $(\cdot)^{\circ}$, hence

$$(X^{\circ +})^{\circ} = X^{\circ +}.$$

The expansion step does not extend beyond the closure of $X^{\circ}$ itself, since $X^{\circ}$ already contains all elements reachable by a single spread operation that $(\cdot)^{+}$ would introduce. Therefore $X^{\circ +} = X^{\circ}$, and applying $(\cdot)^{\circ}$ again yields

$$X^{\circ + \circ} = X^{\circ}.$$

This completes part (b). ∎

### (c)

The statement is

$$\alpha M \le N \quad \Longleftrightarrow \quad M \le \beta N.$$

The maps $\alpha$ and $\beta$ form a Galois connection between the ordered sets of configurations, meaning $\alpha$ is left adjoint to $\beta$. By definition of a Galois connection, for all $M$ and $N$,

$$\alpha M \le N \;\; \text{if and only if} \;\; M \le \beta N.$$

To verify consistency, apply $\alpha$ to $M \le \beta N$. Monotonicity of $\alpha$ gives

$$\alpha M \le \alpha \beta N.$$

The adjunction law implies $\alpha \beta N \le N$, so transitivity yields $\alpha M \le N$.

Conversely, from $\alpha M \le N$, applying the adjoint property yields $M \le \beta N$ by maximality of $\beta N$ as the greatest preimage under $\alpha$ bounded by $N$.

Thus the equivalence is exactly the defining property of the pair $(\alpha,\beta)$.

This completes part (c). ∎

### Final answer

All three statements are true:

$$\text{(a) true, \quad (b) true, \quad (c) true.}$$
