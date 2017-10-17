# jloglevel

[![Build Status](https://travis-ci.org/ivanyu/jloglevel.svg?branch=master)](https://travis-ci.org/ivanyu/jloglevel)

`jloglevel` is a command line tool for changing the logging level in JVM apps in runtime via [Jolokia](https://jolokia.org/).

## How it works

JVM has a technology [Java Management Extensions (JMX)](https://en.wikipedia.org/wiki/Java_Management_Extensions) that allows to monitor and manage JVM applications in runtime. This is done via components called MBeans (managed beans). MBeans have attributes that can be read and operations (methods) that can be executed with JMX.

JVM logging libraries expose MBeans which apart from other features allow control of the logging level in runtime. That means that we can change the logging level of loggers inside the application without restart or modification of files.

JMX has a drawback: it doesn't go well with firewalls, especially in dynamic cloud environments. To overcome this issues, JMX-HTTP bridges exist, and [Jolokia](https://jolokia.org/) is probably the most popular of them. It exposes JMX MBeans over HTTP and allows us to read attributes and call methods using simple GETs and POSTs.

Combining all this together, jloglevel makes it easy to get and set the logging level on a number of JVM applications (e.g. a scaled-out service).

Currently, only [Logback](https://logback.qos.ch/)'s `ROOT` logger is supported.

## Installation

```bash
$ pip3 install jloglevel
```

## Usage prerequisites

1. Jolokia agent needs to be attached to a JVM (or JVMs) you are going to work with. Follow the [Jolokia documentation](https://jolokia.org/documentation.html) for the details.

2. Logback must be configured to expose its control via JMX.
Technically only `<jmxConfigurator />` needs tp be added to `logback.xml`. See [JMX Configurator page](https://logback.qos.ch/manual/jmxConfig.html) in the documentation for the details.

## Usage 

To get the logging levels:

```bash
$ jloglevel get -h 192.168.2.1:8778 -h 192.168.2.2:8778 -h 192.168.2.3:8778

http://192.168.2.1:8778/	DEBUG
http://192.168.2.2:8778/	DEBUG
http://192.168.2.3:8778/	DEBUG
```

Here, `192.168.2.x` and `8778` are the IP addresses and ports where Jolokia agent is listening for incoming connections.

And to set the loggin levels:


```bash
$ jloglevel set -h 192.168.2.1:8778 -h 192.168.2.2:8778 -h 192.168.2.3:8778 TRACE

http://192.168.2.1:8778/	OK
http://192.168.2.2:8778/	OK
http://192.168.2.3:8778/	OK
```

Starting from this moment, the logging level of the ROOT logger is `TRACE`.

SOCKS5 proxying is supported via `--socks5` option:

```bash
$ jloglevel get -h 192.168.2.1:8778 --socks5 127.0.0.1:9999
```

This might be useful with SSH.

## Authors and Contributors

The project is started and maintained by [Ivan Yurchenko](https://ivanyu.me/) (ivan0yurchenko@gmail.com).

Contributions are welcome!

## License

```
Copyright 2017 Ivan Yurchenko

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
