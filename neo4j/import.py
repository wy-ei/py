#coding=utf-8

import sys
import json
import os
import logging
import glob

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')


def build_command_argument(config):
    database = config.get('database', '')

    nodes = config.get('nodes', [])
    relationships = config.get('relationships', [])

    delimiter = config.get('delimiter', ',')
    array_delimiter = config.get('array-delimiter', ';')
    quote = config.get('quote', '"')
    ignore_duplicate_nodes = config.get('ignore-duplicate-nodes', False)
    ignore_missing_nodes = config.get('ignore-missing-nodes', False)
    multiline_field = config.get("multiline_field", False)

    cmd = ''

    if database:
        cmd += ' --database=' + database

    cmd += ' ' + build_nodes_arguments(nodes)

    cmd += ' ' + build_relationships_arguments(relationships)

    cmd += " --delimiter={0}{1}{0}".format('"', delimiter)
    cmd += " --array-delimiter {0}{1}{0}".format('"', array_delimiter)

    if quote != '"':
        cmd += " --quote {0}{1}{0}".format('"', quote)
    if ignore_duplicate_nodes:
        cmd += " --ignore-duplicate-nodes=true"
    if ignore_missing_nodes:
        cmd += " --ignore-missing-nodes=true"
    if multiline_field:
        cmd += " --multiline-fields=true"

    return cmd


def assert_file_exists(file):
    matched_files = glob.glob(file)
    if not matched_files:
        message = 'has no matched file for pattern: ' + file
        logging.error(message)
        exit(-1)


def build_nodes_arguments(nodes):
    if not nodes:
        logging.error('Except at least one node file, but zero founded.')

    arg = ''
    for node in nodes:
        labels = node.get('labels', [])
        header = node.get('header', '')
        file = node.get('file', '')

        if labels:
            arg += ' --nodes:{}='.format(':'.join(labels))
        else:
            arg += ' --nodes='

        files = []
        if header:
            assert_file_exists(header)
            files.append(header)

        assert_file_exists(file)
        files.append(file)

        arg += '"{}"'.format(",".join(files))

    return arg


def build_relationships_arguments(relationships):
    arg = ''
    for relation in relationships:
        types = relation.get('types', [])
        header = relation.get('header', '')
        file = relation.get('file', '')

        if types:
            arg += ' --relationships:{}='.format(':'.join(types))
        else:
            arg += ' --relationships='

        files = []
        if header:
            assert_file_exists(header)
            files.append(header)

        assert_file_exists(file)
        files.append(file)

        arg += '"{}"'.format(",".join(files))

    return arg


def print_usage():
    logging.info('usage:\n\n    python import.py config.json')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_usage()
        sys.exit()

    config_file = sys.argv[1]

    with open(config_file, encoding='utf-8') as fin:
        config = json.load(fin)

    cmd_argument = build_command_argument(config)

    neo4j_home = config['neo4j_home']

    if not neo4j_home:
        logging.error('neo4j_home must be specified.')
        sys.exit()

    os.environ['NEO4J_HOME'] = neo4j_home

    cmd = neo4j_home + '/bin/neo4j-admin import ' + cmd_argument

    # print(cmd)
    os.system(cmd)
