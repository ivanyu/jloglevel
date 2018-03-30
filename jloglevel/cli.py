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

socks5_option = click.option('--socks5', default=None)


@cli.command(name='list-loggers')
@host_option
@socks5_option
def list_loggers_cmd(host, socks5):
    # host is plural (Click limitation).

    """List loggers on the host."""

    request_params = create_request_params(socks5)

    for h in host:
        h = normalise_host(h)
        list_loggers_url = create_list_loggers_url(h)
        try:
            response = requests.get(list_loggers_url, **request_params)
            response.raise_for_status()
            click.echo(make_green(h))
            for log_level in response.json()['value']:
                click.echo(log_level)
            # click.echo()
        except Exception as e:
            click.echo(e, err=True)


@cli.command(name='get')
@host_option
@socks5_option
@click.option('-l', '--logger',
              help='The name of the logger to get the logging level of.',
              default='ROOT')
def get_cmd(host, socks5, logger):
    # host is plural (Click limitation).

    """Gets the logging level from hosts."""

    request_params = create_request_params(socks5)

    click.echo('Logger {}'.format(make_green(logger)))

    for h in host:
        h = normalise_host(h)
        get_url = create_get_url(h, logger)
        try:
            response = requests.get(get_url, **request_params)
            response.raise_for_status()
            log_level = response.json()['value'] or '--'
            click.echo('{}\t{}'.format(h, make_green(log_level)))
        except Exception as e:
            click.echo(e, err=True)
            click.echo(
                '{}\t{}'.format(h, make_red('error getting loglevel'))
            )


@cli.command(name='set')
@host_option
@socks5_option
@click.option('-l', '--logger',
              help='The name of the logger to set the logging level of.',
              default='ROOT')
@click.argument('level',
                type=click.Choice(['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR']))
def set_cmd(host, socks5, logger, level):
    # host is plural (Click limitation).

    """Sets the logging level on hosts."""

    request_params = create_request_params(socks5)

    click.echo('Logger {}'.format(make_green(logger)))

    for h in host:
        h = normalise_host(h)
        set_url = create_set_url(h)
        try:
            json = {
                'type': 'EXEC',
                'mbean': MBEAN,
                'operation': 'setLoggerLevel',
                'arguments': [logger, level]
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


def create_list_loggers_url(host):
    path = ('jolokia/read/{}/LoggerList'.format(MBEAN))
    split_result = urllib.parse.urlsplit(host)
    schema = split_result[0]
    netloc = split_result[1]
    return urllib.parse.urlunsplit([schema, netloc, path, '', ''])


def create_get_url(host, logger):
    path = ('jolokia/exec/{}/getLoggerLevel/{}'.format(MBEAN, logger))
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


# if __name__ == '__main__':
#     cli()
