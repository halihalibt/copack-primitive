# Verified Stable Studionet records

Contract: [`0x467b8a2D10c00b8604efe3d84a9E083E97c8c783`](https://explorer-studio.genlayer.com/address/0x467b8a2D10c00b8604efe3d84a9E083E97c8c783)

- Network: Stable Studionet, chain 61999, RPC `https://studio.genlayer.com/api`.
- Exact deployed source SHA256: `60816f215cf6f52ed19a9cfecc642faeeac2a54aef24aa4011d9a6a5bee0aadf`.
- Source bytes were read from the deployed contract and matched the canonical file exactly.
- All seven listed transactions are FINALIZED, successful, Normal / Full Consensus, with MAJORITY_AGREE. Idle voters are retained; majority agreement is not unanimity.
- No appeal, configured rotation or automatic transaction resubmission was used. Transaction value and gas price were zero. No user wallet or user private key was used.

## Real transactions

| Operation | Transaction | Finality | Leader execution | Votes |
| --- | --- | --- | --- | --- |
| deploy | [0x3fb0f746f9…](https://explorer-studio.genlayer.com/tx/0x3fb0f746f9def79201aa6438970e2c9a908fea0503b6ef4afb3358990f9dc613) | FINALIZED | SUCCESS | 3/5 AGREE |
| optimal:seal | [0x25201f3ad8…](https://explorer-studio.genlayer.com/tx/0x25201f3ad80350d6f4371b57ebd57306b4857ccedf2747e0073363ce11c347ab) | FINALIZED | SUCCESS | 5/5 AGREE |
| optimal:analyze | [0x61982976c6…](https://explorer-studio.genlayer.com/tx/0x61982976c6d97e574704ab261f2f2354536489ce6ce2a75d7814d087a9d84610) | FINALIZED | SUCCESS | 3/5 AGREE |
| review:seal | [0x4b7b66a3a4…](https://explorer-studio.genlayer.com/tx/0x4b7b66a3a4ffe41663518a14c844608d4b14173bdb28709929c5fbe7da1b6f6a) | FINALIZED | SUCCESS | 3/5 AGREE |
| review:analyze | [0xe00d98033f…](https://explorer-studio.genlayer.com/tx/0xe00d98033fd96e2dac0dd6504ce50e297f0126bb323a8edcb9a8e25c0ece234e) | FINALIZED | SUCCESS | 3/5 AGREE |
| robust:seal | [0xf4df8911fc…](https://explorer-studio.genlayer.com/tx/0xf4df8911fcd35890a3014f08a9f8e0504427eda0b7b0d7dd4c198ba7380e9f48) | FINALIZED | SUCCESS | 3/5 AGREE |
| robust:analyze | [0xefcd6ffcda…](https://explorer-studio.genlayer.com/tx/0xefcd6ffcdab94f0a1f9b8fb6eec6b38a0af35571e6c542cb67bced675cb68858) | FINALIZED | SUCCESS | 3/5 AGREE |

## Finalized state readback

| Record ID | Record owner | Accepted business state |
| --- | --- | --- |
| optimal | `0xCF81Ce0Ba3D6e62B8bd7D505E1C51686bA645eAd` | OPTIMAL |
| review | `0xCF81Ce0Ba3D6e62B8bd7D505E1C51686bA645eAd` | REVIEW |
| robust | `0xCF81Ce0Ba3D6e62B8bd7D505E1C51686bA645eAd` | OPTIMAL |

The basic example needs exactly two bins. The two-item unknown case has possible minimum 1 and safe minimum 2, so it remains REVIEW. With both sizes 2 and capacity 2, both minima are 2: the unknown relation cannot improve the packing, and safe singleton bins are robustly OPTIMAL.

`npm run read` makes only reads: it validates chain identity, current receipts, majority evidence, successful leader execution, exact transaction intent, deployed source, finalized records, and input/result hashes. `python scripts/verify_proof.py` independently checks all captured mathematical certificates, without calling the model or network.

## Evidence formats

`evidence/live.json` contains inputs, accepted interpretations, finalized readbacks and explicitly selected original receipt fields. `evidence/raw-live.json.gz` preserves the complete unmodified original journal, including raw RPC receipts and node diagnostics. Archive SHA256: `3573a62258bf57542bf786a0c63f2e0a27cd5998fb0d67536369847166f12a5d`. Decompress with `gzip -dc evidence/raw-live.json.gz`.

`evidence/schema.json` is the real Stable Studio schema compilation response. Compilation alone is not proof of live consensus.

## Local simulation scope

10 Python unit tests passed. Their model and SDK are explicit substitutes. They include a separate exhaustive mathematical oracle and material validator-disagreement cases. The receipt-gate test accepts the recorded success shape and rejects nine false-success conditions (including finality without agreement, missing votes, unsuccessful execution and leader-only mode). These tests are not live consensus evidence.

## Limits of this run

Three small synthetic business cases were executed. This is not a general language benchmark or a proof of provider independence. Test signer secrets were held only in process memory and discarded; the public records remain readable, but the same test identities cannot author new records after process exit.
