
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


def get_client(quiet=False, debug=False):
    '''
       get the client and perform imports not on init, in case there are any
       initialization or import errors. 

       Parameters
       ==========
       quiet: if True, suppress most output about the client
       debug: turn on debugging mode

    '''
    from spython.utils import get_singularity_version
    from .base import Client as client

    client.quiet = quiet
    client.debug = debug

    # Do imports here, can be customized
    from .apps import apps
    from .build import build
    from .execute import (execute, shell) 
    from .help import helpcmd
    from .inspect import inspect
    from .instances import (list_instances, stopall) # global instance commands
    from .run import run
    from .pull import pull
    from .export import (export, _export)

    # Actions
    client.apps = apps
    client.build = build
    client.execute = execute
    client.export = export
    client._export = _export
    client.help = helpcmd
    client.inspect = inspect
    client.instances = list_instances
    client.run = run
    client.shell = shell
    client.pull = pull

    # Command Groups, Images
    from spython.image.cmd import generate_image_commands  # deprecated
    client.image = generate_image_commands()

    # Commands Groups, Instances
    from spython.instance.cmd import generate_instance_commands  # instance level commands
    client.instance = generate_instance_commands()
    client.instance_stopall = stopall
    client.instance.version = client.version

    # Commands Groups, OCI (Singularity version 3 and up)
    if "version 3" in get_singularity_version():
        from spython.oci.cmd import generate_oci_commands
        client.oci = generate_oci_commands()()  # first () runs function, second
                                                # initializes OciImage class
        client.oci.debug = client.debug
        client.oci.quiet = client.quiet
        client.oci.OciImage.quiet = client.quiet
        client.oci.OciImage.debug = client.debug


    # Initialize
    cli = client()

    # Pass on verbosity
    for subclient in [cli.image, cli.instance]:
        subclient.debug = cli.debug
        subclient.quiet = cli.quiet
        subclient.version = cli.version

    return cli

Client = get_client()
