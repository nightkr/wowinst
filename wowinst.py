# !/usr/bin/python3

import os
import shutil
import zipfile
import logging
import argparse

REPO = os.path.abspath(os.path.expanduser("~/.wowrepo"))
WOW = os.path.abspath(os.path.expanduser("~/Games/World of Warcraft/Interface/addons-wowinst"))


def repo_path(name, version=None):
    joined = os.path.join(REPO, name)
    if version:
        joined = os.path.join(joined, version)
    return joined


def canonical_path(x):
    x = os.path.abspath(x)
    if os.path.islink(x):
        link = os.readlink(x)
        if os.path.isabs(link):
            return link
        else:
            return os.path.join(os.path.dirname(x), link)
    else:
        return x


def install(archive_path, name, version):
    install_path = repo_path(name, version)
    if os.path.exists(install_path):
        logging.warning('%s v%s already installed, ignoring', name, version)
        return
    logging.info("Installing %s v%s", name, version)
    os.makedirs(install_path)
    with zipfile.ZipFile(archive_path) as archive:
        archive.extractall(path=install_path)


def uninstall(name, version):
    disable(name, version)
    logging.info("Removing %s v%s", name, version)
    shutil.rmtree(repo_path(name, version))


def versions(name):
    return os.listdir(repo_path(name))


def enabled(name, version=None):
    return [x for x in os.listdir(WOW)
            if canonical_path(os.path.join(WOW, x)).startswith(repo_path(name, version))]


def enable(name, version):
    target = repo_path(name, version)
    for x in os.listdir(target):
        install_target = os.path.join(WOW, x)
        if os.path.exists(install_target):
            logging.warn('%s from %s v%s already enabled, ignoring', x, name, version)
            continue
        logging.info("Enabling %s from %s v%s", x, name, version)
        os.symlink(os.path.join(target, x), install_target)


def disable(name, version):
    for x in enabled(name, version):
        logging.info("Disabling %s from %s v%s", x, name, version)
        os.remove(os.path.join(WOW, x))


def cmd_install(args):
    install(args.path, args.name, args.version)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_install = subparsers.add_parser('install')
    parser_install.add_argument('path', type=str)
    parser_install.add_argument('name', type=str)
    parser_install.add_argument('version', type=str)
    parser_install.set_default(func=cmd_install)

    parser_uninstall = subparsers.add_parser('uninstall')
    parser_uninstall.add_argument('name', type=str)
    parser_uninstall.add_argument('version', type=str)

    args = parser.parse_args()
    args.func(args)
