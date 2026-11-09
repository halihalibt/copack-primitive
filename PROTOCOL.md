# CoPack: bounds and optimality

## Inputs and semantic graph

The input contains 2–8 distinct item descriptions, positive integer sizes, a shared capacity 1–100, and an explicit pairwise-only policy. Each size is no greater than capacity, so a singleton bin is always feasible. Pairs are ordered lexicographically: (0,1), (0,2), ..., (n-2,n-1). The leader and validators independently classify all pairs ALLOW, BLOCK or UNKNOWN. Size arithmetic is excluded by rule from semantic pair classification: an overflowing pair may still be semantically allowed.

Descriptions and constraints are caller-authored. Pairwise compatibility does not establish higher-order or physical safety. Unsupported three-item interactions must remain UNKNOWN; callers should not use this finite model for hazardous material decisions.

## Two exact problems

The safe problem permits only ALLOW pairs; UNKNOWN and BLOCK pairs cannot share a bin. The possible problem additionally permits UNKNOWN. Each subset is feasible when its total size is at most capacity and every contained pair is permitted in that problem.

Let F(mask) be the smallest number of bins needed for mask. F(0)=0. For each nonempty mask, enumerate every feasible submask containing the lowest-index item of mask and take `min(1 + F(mask \ submask))`. Any partition has exactly one bin containing that item, so this symmetry reduction omits no solution. Every remaining mask is smaller, making the table an acyclic dynamic program. Ascending subset masks give deterministic tie-breaking. The full cost table and all feasible masks accompany the canonical bins.

The possible minimum is a lower bound on every resolution of UNKNOWN. The safe minimum is an upper bound, and its bins require no unknown permission. If these numbers match, those safe bins are robustly optimal (OPTIMAL), even if an irrelevant unknown remains. Otherwise REVIEW returns a safe plan and the exact uncertainty interval; no exact optimum is claimed.

## Checking the proof

Check each bin contains distinct valid item indices, every item occurs once, capacity is respected, and every co-binned pair is ALLOW for the safe plan. Re-enumerate feasible masks and each Bellman recurrence to establish optimality for both graphs. A small independent set-partition enumerator in the tests verifies the DP on every four-item binary compatibility graph.

## State and hashes

`SEALED -> OPTIMAL | REVIEW`, revision 0 -> 1. A terminal record includes the entire accepted pair vector, both proofs, immutable input and a SHA256 result commitment bound to protocol, owner and record ID. There is no reservation, shipment, pricing, item splitting or funds transfer.
