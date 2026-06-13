---
title: "CF 1534H - Lost Nodes"
description: "Consider a closed container of fixed volume $V$ containing an ideal gas whose bulk temperature is $T1$. The container walls are maintained at temperature $T$, and $T$ need not equal $T1$."
date: "2026-06-10T16:07:15+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp", "graphs", "interactive", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1534
codeforces_index: "H"
codeforces_contest_name: "Codeforces LATOKEN Round 1 (Div. 1 + Div. 2)"
rating: 3500
weight: 1534
solve_time_s: 92
verified: false
draft: false
---

[CF 1534H - Lost Nodes](https://codeforces.com/problemset/problem/1534/H)

**Rating:** 3500  
**Tags:** constructive algorithms, dp, graphs, interactive, sortings, trees  
**Solve time:** 1m 32s  
**Verified:** no  

## Solution
## Setup and Assumptions

Consider a closed container of fixed volume $V$ containing an ideal gas whose bulk temperature is $T_1$. The container walls are maintained at temperature $T$, and $T$ need not equal $T_1$. The problem asks for the instantaneous pressure exerted by the gas on the walls when the gas and walls are not in thermal equilibrium.

The essential point is that molecules arriving at the wall come from the gas and have a velocity distribution corresponding to $T_1$, while molecules leaving the wall after accommodation to the wall temperature have a velocity distribution corresponding to $T$. Since pressure is the rate of momentum transfer to the wall, both temperatures enter the calculation.

Assume complete thermal accommodation at the wall. Molecules striking the wall are characterized by temperature $T_1$, and molecules re-emitted from the wall are characterized by temperature $T$. The gas is sufficiently rarefied that kinetic-theory expressions for molecular fluxes may be used locally at the wall.

Because the vessel is closed and mechanical equilibrium is established much faster than thermal equilibrium, the pressure $P$ is a single quantity throughout the gas. The molecular density adjacent to the wall is not an externally prescribed constant; it adjusts so that the same pressure acts everywhere in the vessel. The calculation below determines the relation between $P$, $T$, and the wall density $n$.

## Physical Principles

The pressure on a wall equals the normal momentum transferred to that wall per unit area and per unit time.

Let $n$ be the molecular number density adjacent to the wall. For a Maxwellian gas of temperature $T_1$, the flux of molecules striking a unit area of wall per unit time is

$$\Phi_{\rm in}=n\sqrt{\frac{k_B T_1}{2\pi m}},$$

where $m$ is the molecular mass.

The average normal momentum carried by an incident molecule is

$$\langle p_x\rangle_{\rm in} = \frac{\displaystyle\int_0^\infty m v_x^2 e^{-m v_x^2/(2k_B T_1)}\,dv_x} {\displaystyle\int_0^\infty v_x e^{-m v_x^2/(2k_B T_1)}\,dv_x} = \sqrt{\frac{\pi m k_B T_1}{2}}.$$

Multiplying the incident flux by the average momentum per incident molecule gives

$$J_{\rm in} = n\sqrt{\frac{k_B T_1}{2\pi m}} \sqrt{\frac{\pi m k_B T_1}{2}} = \frac12 n k_B T_1.$$

Molecules leaving the wall have temperature $T$. Let their number density just at emission be $n_w$. Repeating the same calculation for the emitted Maxwellian gives

$$J_{\rm out} = \frac12 n_w k_B T.$$

The pressure on the wall is the sum of the magnitudes of the incoming and outgoing momentum fluxes:

$$P=J_{\rm in}+J_{\rm out}.$$

A stationary wall cannot accumulate molecules. The number of molecules arriving at the wall per unit area and unit time must equal the number leaving it. Hence

$$n\sqrt{\frac{k_B T_1}{2\pi m}} = n_w\sqrt{\frac{k_B T}{2\pi m}},$$

which yields

$$n_w=n\sqrt{\frac{T_1}{T}}.$$

## Derivation

Substituting

$$n_w=n\sqrt{\frac{T_1}{T}}$$

into the expression for the outgoing momentum flux gives

$$J_{\rm out} = \frac12 n\sqrt{\frac{T_1}{T}}\,k_B T = \frac12 n k_B\sqrt{T_1T}.$$

The incoming flux remains

$$J_{\rm in} = \frac12 n k_B T_1.$$

Hence

$$P = \frac12 n k_B T_1 + \frac12 n k_B\sqrt{T_1T} = \frac12 n k_B\left(T_1+\sqrt{T_1T}\right).$$

At this stage $n$ is the density adjacent to the wall. Since the pressure in the closed vessel is the unique mechanical pressure, this relation may be solved for the wall density:

$$n = \frac{2P} {k_B\left(T_1+\sqrt{T_1T}\right)}.$$

For a fixed pressure $P$ and fixed gas temperature $T_1$, increasing the wall temperature decreases the wall density according to this formula. The wall density adjusts precisely so that the same pressure is maintained.

The expression for $P$ derived above is therefore not a prediction that the pressure changes when $T$ changes. It is a relation between $P$ and the local density $n$. Since $n$ is not fixed independently in a closed container, one cannot compare pressures at different wall temperatures by treating $n$ as constant.

The pressure is determined by the state of the gas in the vessel, whereas the wall temperature modifies the density of the Knudsen layer adjacent to the wall.

## Result

The kinetic-theory calculation gives

$$P = \frac12 n k_B\left(T_1+\sqrt{T_1T}\right),$$

where $n$ is the molecular density adjacent to the wall.

In a closed container, $n$ is not fixed when $T$ changes. Instead,

$$n = \frac{2P} {k_B\left(T_1+\sqrt{T_1T}\right)}$$

adjusts so that the same mechanical pressure exists throughout the vessel.

Consequently, the calculation does not support the claim that the pressure is larger for $T>T_1$ or smaller for $T<T_1$. The pressure can remain the same while the near-wall density changes. From the information given in the problem, neither inequality

$$P(T>T_1)>P(T<T_1)$$

nor

$$P(T>T_1)<P(T<T_1)$$

is established.

The correct conclusion from the kinetic-theory analysis is that hotter walls correspond to a lower wall-adjacent density and colder walls correspond to a higher wall-adjacent density, while the pressure itself is not determined by the wall temperature alone.

## Sanity Checks

When $T=T_1$,

$$P = \frac12 n k_B(T_1+T_1) = n k_B T_1,$$

which is the standard ideal-gas pressure.

Solving for $n$ gives

$$n=\frac{P}{k_B T_1},$$

again reproducing the equilibrium ideal-gas relation.

When $T\to0$,

$$P = \frac12 n k_B T_1,$$

and therefore

$$n=\frac{2P}{k_B T_1}.$$

The wall density is twice the equilibrium value required to maintain the same pressure.

When $T\gg T_1$,

$$P \sim \frac12 n k_B\sqrt{T_1T},$$

so

$$n \sim \frac{2P}{k_B\sqrt{T_1T}}.$$

The wall density decreases as $T^{-1/2}$ while the pressure remains finite.

These limiting cases are consistent with the interpretation that wall temperature changes the density in the immediate vicinity of the wall rather than directly determining the pressure of the closed vessel.
