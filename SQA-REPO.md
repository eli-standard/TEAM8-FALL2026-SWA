#Report



#4.a



#4.b



#4.c
For the CI job we decided to go out of the way a little and add RUFF as a lint check to the actions. Eli added this as he uses it for work, and, in general, running a basic linter is good practice especially at the start of a CI job. RUFF has a few rules for syntax/undefined names that will fail that job, but there is a second run that just reports other warnings and output them without fully failling it. We added the already existing tests (TEST_SCANNING, TEST_INTEGRATION, TEST_GRAPH, TEST_PARSING) even though they will fail due to the constants those first three use being not available. Using the continue-on-error flag we'll show that these fail, but the rest of the ci job will continue instead of stopping so the hypothetical user would be able to see everything wrong at once. 