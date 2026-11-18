#Report



#4.a



#4.b



#4.c
For the CI job we started with getting the dependencies needed to run the tests that were in the repo. These dependencies just had to be found by seeing what files the tests relied on and seeing what dependencies those had. We decided to go out of the way a little and add RUFF as a lint check to the actions. Eli added this as he uses it for work, and, in general, running a basic linter is good practice especially at the start of a CI job. RUFF has a few rules for syntax/undefined names that will fail that job, but there is a second run that just reports other warnings and outputs them without fully failling it. We added the already existing tests (TEST_SCANNING, TEST_INTEGRATION, TEST_GRAPH, TEST_PARSING), but since those first three will fail due to the lack of the required constants (they have a local path not available to us) we used the continue-on-error flag which will continue to the next job instead of stopping so the hypothetical user would be able to see everything wrong at once instead of having to run the ci job multiple time just to figure out each test would fail. 