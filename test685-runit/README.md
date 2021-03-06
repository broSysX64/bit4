# User service management with runit

## Service directory

The service directory structure is the same as that of daemontools:

    service/
      icecast/
        run*
        log/
          run*

The service script would look like this:

    #!/bin/sh
    exec 2>&1
    exec icecast -c icecast.xml

The logger script would look like this:

    #!/bin/sh
    exec svlogd -ttt .

The `-ttt` option instructs `svlogd` (runit's `multilog` equivalent) to record
timestamp in the ISO 8601 format.

## Service dependency

In this example the dummy service `caster` depends on `icecast`. This is
expressed in the service script of `caster` as follows:

    #!/bin/sh
    sv start ../icecast || exit 1
    ...

This ensures `icecast` to have started before `caster`.

See: http://smarden.org/runit/faq.html#depends

## Launching supervisors

Use user's crontab to let supervisors start at boot time:

    @reboot runsvdir ~/service

Execute the same command in a fresh tmux session and detach the session to
launch supervisors without actual reboot.

Note: The example above discards any error messages from `runsvdir`. Maybe the
output should be piped to `svlogd` and logged somewhere.

## Service management

Set environment variable `SVDIR` to the service directory and use `sv` command
to manage services.

    sv status icecast
    sv down icecast
    sv up icecast

View service log:

    less $SVDIR/icecast/log/current
