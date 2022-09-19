# Total Perspective Vortex

![Total Perspective Vortex Logo](logo/logo.png)

Configures services based on templates and a YAML config file, just like the
name suggests!

Designed with routers and local networks in mind.

Copyright (C) 2018 Joey Parrish <joey.parrish@gmail.com>

Released under the GNU GPL v3 license.


## Why?

I built a Linux router and firewall at home, but I didn't like any of the
web-based router management interfaces I looked at.  So I decided that I wanted
to maintain it over SSH with a text editor.  I also didn't want to duplicate
information about hosts in multiple config files for multiple services (DHCP &
DNS, for example).  I wanted one place to put host metadata and one command to
update everything.

What I built is more generic than that, though.  You can use it to generate
config files for anything and reload any service with any command afterward.


## Quick Installation

```sh
cp total-perspective-vortex /usr/local/bin/
mkdir /etc/total-perspective-vortex/
# Now read sample-config.yaml and sample-templates/ and take what you need
# for your own setup in /etc/total-perspective-vortex/ .  Make up your own
# templates as needed.
```


## Usage

1. Modify YAML config file.
2. Run `sudo total-perspective-vortex --diff` to see a diff of what will change.
3. Run `sudo total-perspective-vortex` to generate output from templates and
   reload services.


## YAML Config File

The YAML config file is for you to store metadata describing your network or
whatever else you are configuring.  The structure and contents of the file is
completely arbitrary, but it contains only static data, not logic.

You can put whatever you want in that file using any names you like, except for
the three reserved names used by the Total Perspective Vortex in template files:
  - output_path
  - output_mode
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

Each template can set three reserved variables as output to the tool:

### output_path

The output_path variable is **required** to be set in each template.  This tells
the Total Perspective Vortex where to put the generated output from the
template.

Example:

```jinja2
{% set output_path = '/etc/bind/db.home' %}
```

### output_mode

The output_mode variable is optional.  If present, it tells the Total
Perspective Vortex what file mode to set on the output.  If missing, it will
default to `0644` (world-readable, not executable).  The values for output_mode
should be expressed in octal, but should be set as a string in the template.

Example:

```jinja2
{% set output_mode = '700' %}
```

### service_reload

The service_reload variable is optional.  If present, it tells the Total
Perspective Vortex what commands to execute to reload services after generating
the output.

Service reloading happens after all templates have been processed and all output
has been generated.  If two templates contain identical reload commands, the
command will only be executed once.

Example:

```jinja2
{% set service_reload = 'ufw enable && ufw reload' %}
```

## Logo

The Total Perspective Vortex logo is based on
["Cupcake (34)"](https://www.svgrepo.com/svg/65988/cupcake)
by ["SVG Repo"](https://www.svgrepo.com/)
(License: [CC0](https://www.svgrepo.com/page/licensing))

The path is repeated using SVG defs, generated from a script.
See [logo/gen.py](https://github.com/joeyparrish/total-perspective-vortex/blob/main/logo/gen.py)
