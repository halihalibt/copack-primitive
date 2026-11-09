import importlib.util
import json
from pathlib import Path
import sys
import types
import unittest
from copy import deepcopy

class Return:
    def __init__(self, value):
        self.calldata = value

class Storage(dict):
    @classmethod
    def __class_getitem__(cls, _):
        return cls

def identity(f):
    return f

gl = types.SimpleNamespace(Contract=object, public=types.SimpleNamespace(view=identity, write=identity),
    message=types.SimpleNamespace(sender_address="0x"+"1"*40),
    vm=types.SimpleNamespace(Return=Return), nondet=types.SimpleNamespace())
sdk = types.ModuleType("genlayer")
sdk.gl, sdk.TreeMap, sdk.u32 = gl, Storage, int
sys.modules["genlayer"] = sdk
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("contract", ROOT/"contracts"/"copack.py")
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
BASIC = json.loads((ROOT/"examples/basic.json").read_text())

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.data = deepcopy(BASIC)
        gl.message.sender_address = "0x"+"1"*40
        self.obj = c.CoPack()
        self.obj.records, self.obj.counts = {}, {}

    def consensus(self, leader, validator=None):
        responses = iter([leader, leader if validator is None else validator])
        gl.nondet.exec_prompt = lambda *a, **k: json.dumps(next(responses))
        def run(fn, check):
            answer = fn()
            if not check(Return(answer)):
                raise Exception("CONSENSUS_REJECTED")
            return answer
        gl.vm.run_nondet_unsafe = run

    def test_namespaces_and_idempotency(self):
        key = self.obj.seal("sample", json.dumps(self.data))
        self.assertEqual(key, self.obj.seal("sample", json.dumps(self.data)))
        self.assertEqual(self.obj.counts["0x"+"1"*40], 1)
        gl.message.sender_address = "0x"+"2"*40
        self.assertEqual(self.obj.get_record(str(gl.message.sender_address), "sample"), "")
        with self.assertRaisesRegex(Exception,"NOT_FOUND"):
            self.obj.analyze("sample", 0)

    def test_invalid_id_and_json(self):
        for name in ["", "Bad ID", "x"*49]:
            with self.assertRaises(Exception):
                self.obj.seal(name, json.dumps(self.data))
        with self.assertRaisesRegex(Exception,"DUPLICATE_KEY"):
            c.unpack('{"a":1,"a":2}')

    def test_failure_does_not_store_assessment(self):
        key = self.obj.seal("sample", json.dumps(self.data))
        before = deepcopy(self.obj.records)
        gl.nondet.exec_prompt = lambda *a, **k: (_ for _ in ()).throw(Exception("MODEL_UNAVAILABLE"))
        gl.vm.run_nondet_unsafe = lambda leader, validator: leader()
        with self.assertRaisesRegex(Exception,"MODEL_UNAVAILABLE"):
            self.obj.analyze("sample", 0)
        self.assertEqual(before, self.obj.records)

    def test_revision_guard(self):
        self.obj.seal("sample", json.dumps(self.data))
        with self.assertRaisesRegex(Exception,"STALE_REVISION"):
            self.obj.analyze("sample", 1)

    def test_lifecycle_and_exact_two_bin_result(self):
        a={"pairs":["BLOCK","ALLOW","ALLOW"]}
        self.consensus(a)
        self.obj.seal("sample",json.dumps(self.data))
        r=json.loads(self.obj.analyze("sample",0))
        self.assertEqual(r["state"],"OPTIMAL")
        self.assertEqual(r["proof"]["safe"]["minimum"],2)
        self.assertEqual(sorted(i for b in r["proof"]["safe"]["bins"] for i in b),[0,1,2])

    def test_unknown_that_changes_optimum_requires_review(self):
        d={"items":["a","b"],"sizes":[1,1],"capacity":2,"rules":"pairwise"}
        r=c.solve(d,{"pairs":["UNKNOWN"]})
        self.assertEqual((r["status"],r["lower_bound"],r["upper_bound"]),("REVIEW",1,2))

    def test_irrelevant_unknown_still_certifies_robust_optimum(self):
        d={"items":["a","b"],"sizes":[2,2],"capacity":2,"rules":"pairwise"}
        r=c.solve(d,{"pairs":["UNKNOWN"]})
        self.assertEqual((r["status"],r["lower_bound"],r["upper_bound"]),("OPTIMAL",2,2))

    def test_validator_checks_every_pair_even_unchanged_optimum(self):
        self.consensus({"pairs":["BLOCK","ALLOW","ALLOW"]},{"pairs":["BLOCK","BLOCK","ALLOW"]})
        with self.assertRaisesRegex(Exception,"CONSENSUS_REJECTED"):
            c.independent_agreement(self.data,c.parse_answer)

    def test_exact_dp_against_exhaustive_partition_oracle(self):
        import itertools
        n=4
        def partitions(items):
            if not items:
                yield []
                return
            first,*rest=items
            for p in partitions(rest):
                yield [[first]]+[b[:] for b in p]
                for i in range(len(p)):
                    q=[b[:] for b in p];q[i]=[first]+q[i];yield q
        for labels in itertools.product(["ALLOW","BLOCK"],repeat=6):
            lookup={pair:label for pair,label in zip(itertools.combinations(range(n),2),labels)}
            d={"items":[str(i) for i in range(n)],"sizes":[1,2,1,2],"capacity":3}
            valid=[p for p in partitions(list(range(n))) if all(
                sum(d["sizes"][i] for i in b)<=3 and all(lookup[tuple(sorted((i,j)))]=="ALLOW"
                for i,j in itertools.combinations(b,2)) for b in p)]
            r=c.solve(d,{"pairs":list(labels)})
            self.assertEqual(r["safe"]["minimum"],min(map(len,valid)))
            costs=r["safe"]["cost_table"];feasible=set(r["safe"]["feasible_masks"])
            for mask in range(1,1<<n):
                options=[s for s in feasible if s&mask==s]
                self.assertEqual(costs[mask],min(1+costs[mask^s] for s in options))

    def test_size_guards_and_malformed_answers(self):
        for size in [True,0,4]:
            d=deepcopy(self.data);d["sizes"][0]=size
            with self.assertRaises(Exception):c.input_data(d)
        for a in [{"pairs":[]},{"pairs":["ALLOW"]*4},{"pairs":[True]*3}]:
            with self.assertRaises(Exception):c.parse_answer(a,self.data)

if __name__ == "__main__":
    unittest.main()
