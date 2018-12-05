# Total Perspective Vortex

Configures services based on templates and a YAML config file, just like the
name suggests!

Designed with routers and local networks in mind.

Copyright (C) 2018 Joey Parrish <joey.parrish@gmail.com>

Released under the GNU GPL v3 license.


## Quick Installation

```sh
cp total-perspective-vortex /usr/local/bin/
mkdir /etc/total-perspective-vortex/
# Now read sample-config.yaml and sample-templates/ and take what you need
# for your own setup in /etc/total-perspective-vortex/
```


## Usage

1. Modify YAML config file
2. Run `sudo total-perspective-vortex` to generate output from templates and
   reload services.


## YAML Config File

The YAML config file is for you to store metadata describing your network or
whatever else you are configuring.  The structure and contents of the file is
completely arbitrary, but it contains only static data, not logic.

You can put whatever you want in that file using any names you like, except for
the two reserved names used by the Total Perspective Vortex in template files:
  - output_path
  - service_reload

The default location for the config file is
`/etc/total-perspective-vortex/config.yaml`, and you can override that with the
`-c` option.


## Template Files

The Total Perspective Vortex will go through each template file in your
templates folder, combine it with your YAML config data, and generate output.

The template files can contain actual logic to transform the input data, loop
over it for repeated configs, and provide additional information as output.

Template files use the Jinja2 template engine, so you will want to get familiar
with the Jinja documentation here: http://jinja.pocoo.org/docs/

The default location for the templates folder is
`/etc/total-perspective-vortex/templates`, and you can override that with the
`-t` option.

Each template can set two reserved variables as output to the tool:

### output_path

The output_path variable is required to be set in each template.  This tells
the Total Perspective Vortex where to put the generated output from the
template.

### service_reload

The service_reload variable is optional.  If present, it tells the Total
Perspective Vortex what commands to execute to reload services after generating
the output.

Service reloading happens after all templates have been processed and all output
has been generated.  If two templates contain identical reload commands, the
command will only be executed once.
