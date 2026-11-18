#Report



#4.a

The first two fuzz targets are `keyMiner` and `getValuesRecursively`.
`fuzz.py` generates nested dictionaries and lists with varied scalar values
and checks the expected search path and value traversal order. Each method
passed 500 generated cases with seed 42. These cases produced no failures.


#4.b

Forensic logging is integrated into ten methods. Run `python verify_forensics.py`
from `KubeSec-master` to exercise all ten with temporary fixtures and verify that
each emits its expected event. Save the output as execution evidence.

| Module | Methods | Evidence |
| --- | --- | --- |
| parser | `checkParseError`, `loadMultiYAML` | Failure type, document count, and parse outcome |
| parser | `checkIfWeirdYAML`, `checkIfValidK8SYaml`, `checkIfValidHelm` | Path and classification outcome |
| parser | `readYAMLAsStr`, `count_initial_comment_line`, `getSingleDict4MultiDocs` | Character count, header line count, and merged key count |
| graphtaint | `getYAMLFiles`, `getSHFiles` | Directory and file count by type |

The records omit YAML contents. The smoke test verified all ten distinct
events, and all 23 existing parsing tests passed locally.

#4.c
For the CI job we started with getting the dependencies needed to run the tests that were in the repo. These dependencies just had to be found by seeing what files the tests relied on and seeing what dependencies those had. We decided to go out of the way a little and add RUFF as a lint check to the actions. Eli added this as he uses it for work, and, in general, running a basic linter is good practice especially at the start of a CI job. RUFF has a few rules for syntax/undefined names that will fail that job, but there is a second run that just reports other warnings and outputs them without fully failling it. We added the already existing tests (TEST_SCANNING, TEST_INTEGRATION, TEST_GRAPH, TEST_PARSING), but since those first three will fail due to the lack of the required constants (they have a local path not available to us) we used the continue-on-error flag which will continue to the next job instead of stopping so the hypothetical user would be able to see everything wrong at once instead of having to run the ci job multiple time just to figure out each test would fail.
