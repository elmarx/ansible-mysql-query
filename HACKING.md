# Hacking mysql_query module/role

This module is TDD. Although it's sometimes hard to debug and test everything, I think I found a nice setup for TDD-ansible-modules. I'll document this in detail in an upcoming blogpost (TODO: link the blogpost once published).

You can either run all tests inside a vagrant box or directly on your host.

## vagrant

The vagrant box should give you all you need: *python*, latest *ansible*, *mysql* etc. Of course provisioned by an ansible playbook.

I recommend to use pycharm's [remote debugging](http://blog.jetbrains.com/pycharm/2013/03/how-pycharm-helps-you-with-remote-development/) to run tests.

## local

Currently this module only modifies the database, nothing critical, so it's safe to run tests on the host directly. Imagine you develop a module that changes system-files, you would not want the module to modify your host, would you? ;)

For local development/testing you'll need *python*, *ansible* and a *testrunner* (my recommendation: [nose](https://nose.readthedocs.org/en/latest/)). Default Debian-packages are fine. Additionally you'll need a mysql installation with a user that is capable of creating and dropping databases. Of course mysql installed from an apt-repository is fine, but I prefer a docker container to run server software.

### packages to install (Debian)

Just for reference (or the lazy ones), install the following packages for the recommended setup:

- ansible
- docker-engine
- docker-compose
- python
- python-nose

### workflow

Start the mariadb container with *docker-compose*:

    $ cd tests/infrastructure
    $ docker-compose up -d

Then tests are executable via:

    $ ANSIBLE_LIBRARY=$PWD/library MYSQL_HOST=::1 MYSQL_PASSWORD=password nosetests tests/

or configure PyCharm to execute your tests.
