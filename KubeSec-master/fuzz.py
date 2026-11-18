"""Seeded randomized checks for parser traversal helpers."""

from random import Random

from parser import getValuesRecursively, keyMiner


SEED = 42
CASES = 500


def main():
    rng = Random(SEED)
    scalars = [None, False, 0, -1, 3.5, "", "café", "plain text"]

    for case in range(CASES):
        target = f"target-{case}"
        tree = target
        expected_path = [target]
        expected_values = [target]

        for depth in range(rng.randrange(9)):
            before = rng.choices(scalars, k=rng.randrange(4))
            after = rng.choices(scalars, k=rng.randrange(4))
            if rng.choice([True, False]):
                tree = before + [tree] + after
                expected_path.insert(0, str(len(before)))
            else:
                key = f"level-{depth}"
                tree = {"before": before, key: tree, "after": after}
                expected_path.insert(0, key)
            expected_values = before + expected_values + after

        actual_path = keyMiner(tree, target)
        if actual_path != expected_path or keyMiner(tree, "absent") is not None:
            raise AssertionError(f"keyMiner failed with seed {SEED}, case {case}")

        actual_values = list(getValuesRecursively(tree))
        if [(type(value), value) for value in actual_values] != [
            (type(value), value) for value in expected_values
        ]:
            raise AssertionError(
                f"getValuesRecursively failed with seed {SEED}, case {case}"
            )

    print(f"keyMiner and getValuesRecursively passed {CASES} cases each (seed {SEED}).")


if __name__ == "__main__":
    main()
