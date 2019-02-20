These are all the integration tests.

The p8_jenkins_quick directory are those that Jenkins can run with a shorter timeout.

The p8_jenkins_long directory are those that Jenkins can run with a longer timeout.
These should be both intergation tests and speed tests.

The p8_manual directory are useful tests but are often larger version of the ones above and do not need to be run each time by Jenkins.

Allother directories are being reviewed
If they are not moved they are not run and risk being removed forever.