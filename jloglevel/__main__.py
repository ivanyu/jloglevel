#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.parse
import requests
import click


MBEAN = ('ch.qos.logback.classic:Name=default,' +
         'Type=ch.qos.logback.classic.jmx.JMXConfigurator')


@click.group()
def cli():
    pass


host_option = click.option(
    '-h', '--host', multiple=True,
    help='Host (and port if needed) to connect. Can be multiple.')


@cli.command(name='get')
@host_option
@click.option('--socks5', default=None)
def get_cmd(host, socks5):
    # host is plural (Click limitation).

    """Gets the logging level from hosts."""

    request_params = create_request_params(socks5)

    for h in host:
        h = normalise_host(h)
        get_url = create_get_url(h)
        try:
            response = requests.get(get_url, **request_params)
            response.raise_for_status()
            log_level = response.json()['value']
            click.echo('{}\t{}'.format(h, make_green(log_level)))
        except Exception as e:
            click.echo(e, err=True)
            click.echo(
                '{}\t{}'.format(h, make_red('error getting loglevel'))
            )


@cli.command(name='set')
@host_option
@click.option('--socks5', default=None)
@click.argument('level',
                type=click.Choice(['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR']))
def set_cmd(host, socks5, level):
    # host is plural (Click limitation).

    """Sets the logging level on hosts."""

    request_params = create_request_params(socks5)

    for h in host:
        h = normalise_host(h)
        set_url = create_set_url(h)
        try:
            json = {
                'type': 'EXEC',
                'mbean': MBEAN,
                'operation': 'setLoggerLevel',
                'arguments': ['ROOT', level]
            }
            response = requests.post(set_url, json=json, **request_params)
            response.raise_for_status()
            click.echo('{}\t{}'.format(h, make_green('OK')))
        except Exception as e:
            click.echo(e, err=True)
            click.echo(
                '{}\t{}'.format(h, make_red('error setting loglevel'))
            )


def create_request_params(socks5_host):
    request_params = {}
    if socks5_host is not None:
        request_params['proxies'] = create_proxy_dict(socks5_host)
    return request_params


def create_proxy_dict(socks5_host):
    return {
        'http': 'socks5://' + socks5_host,
        'https': 'socks5://' + socks5_host
    }


def normalise_host(host):
    if not host.startswith('http://') and not host.startswith('https://'):
        host = 'http://' + host
    if not host.endswith('/'):
        host = host + '/'
    return host


def create_get_url(host):
    path = ('jolokia/exec/{}/getLoggerLevel/ROOT'.format(MBEAN))
    split_result = urllib.parse.urlsplit(host)
    schema = split_result[0]
    netloc = split_result[1]
    return urllib.parse.urlunsplit([schema, netloc, path, '', ''])


def create_set_url(host):
    path = 'jolokia/exec'
    split_result = urllib.parse.urlsplit(host)
    schema = split_result[0]
    netloc = split_result[1]
    return urllib.parse.urlunsplit([schema, netloc, path, '', ''])


def make_green(string):
    return click.style(string, fg='green')


def make_red(string):
    return click.style(string, fg='red')


if __name__ == '__main__':
    cli()
