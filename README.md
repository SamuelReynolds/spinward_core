Spinward Core
=============

**Copyright © (c) 2000-2020 by Samuel Reynolds. All rights reserved.**

A collection of foundation classes and utilities in Python 3.
Part of the `spinward` project namespace, along with `spinward_source`,
`spinward_transformer`, `spinward_writer` (and others to come).

This software is released under the BSD-3-Clause license
(https://opensource.org/licenses/BSD-3-Clause).


tl;dr:
------
I am in the process of updating these tools from versions originally created
for Python 2 about 10 years ago. This consists of updating them to Python 3
(specifically, 3.8) and improving them based on my experience since they were
originally created.

Only those that have been updated to Python 3.8 and thoroughly unit-tested
are included in the published repository.

All interim work based on those original versions (in Python 2.6/2.7) was
performed for employers under NDA, and are no longer available to me.
As a result, I am making improvements based on my experience over the last
decade and on requirements in my own head. The development trajectory will
not match that of the code I've lost, but hopefully, in the process, the
utilities will benefit from lessons learned.

This development path is also my effort to finish the switch to Python 3.
(It's remarkable how difficult it can be, in the real world of support
and deadlines, to move up from Python 2.7, even after it was retired.)
Some of these utilities may have been obviated by library modules or other
standardized tools in the world of Python 3. Where that is the case, I will
deprecate the affected `spinward_core` utility unless it provides a
significant capability not provided by the newer tools.

I have put minimal effort into `setup.py`; it will almost certainly need work.
That said, `python3 setup.py sdist` does work.
