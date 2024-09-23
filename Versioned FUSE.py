# Install fusepy using: pip install fusepy
import os
import sys
import time
import argparse
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

class VersionedFS(LoggingMixIn, Operations):
    def __init__(self, root):
        self.root = root
        self.versions = {}  # Dictionary to store versions of each file

    def _full_path(self, partial):
        """Translate a partial path to a full path."""
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem operations

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                                                        'st_gid', 'st_mode',
                                                        'st_mtime', 'st_nlink',
                                                        'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self._full_path(path)
        dirents = ['.', '..'] + os.listdir(full_path)
        return dirents

    def read(self, path, size, offset, fh):
        full_path = self._full_path(path)
        with open(full_path, 'rb') as f:
            f.seek(offset)
            return f.read(size)

    def write(self, path, data, offset, fh):
        full_path = self._full_path(path)
        with os.fdopen(os.open(full_path, os.O_RDWR), 'r+b') as f:
            f.seek(offset)
            f.write(data)
            # f.truncate()
        return len(data)

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        fd = os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)
        return fd

    def unlink(self, path):
        full_path = self._full_path(path)
        os.unlink(full_path)

    # Versioning operations

    def create_version(self, path):
        full_path = self._full_path(path)
        if path not in self.versions:
            self.versions[path] = []
        version = time.strftime("%Y%m%d%H%M%S")
        version_path = f"{full_path}.{version}"
        os.system(f"cp {full_path} {version_path}")
        self.versions[path].append(version)
        return version

    def switch_version(self, path, version):
        full_path = self._full_path(path)
        version_path = f"{full_path}.{version}"
        if os.path.exists(version_path):
            os.system(f"cp {version_path} {full_path}")
        else:
            raise FuseOSError(f"Version '{version}' not found for file '{path}'")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Versioned FUSE Filesystem')
    parser.add_argument('root', help='Root directory of the filesystem')
    parser.add_argument('mountpoint', help='Mountpoint directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')

    # Add a subparser for additional commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create a parser for the 'create_version' command
    parser_create_version = subparsers.add_parser('create_version', help='Create a new version of a file')
    parser_create_version.add_argument('file_path', help='Path to the file to version')

    # Create a parser for the 'switch_version' command
    parser_switch_version = subparsers.add_parser('switch_version', help='Switch to a specific version of a file')
    parser_switch_version.add_argument('file_path', help='Path to the file to switch version')
    parser_switch_version.add_argument('version', help='Version to switch to')

    args = parser.parse_args()

    root = args.root
    mountpoint = args.mountpoint

    if args.command == 'create_version':
        # If the 'create_version' command is provided, handle it
        versioned_fs = VersionedFS(root)
        versioned_fs.create_version(args.file_path)
    elif args.command == 'switch_version':
        # If the 'switch_version' command is provided, handle it
        versioned_fs = VersionedFS(root)
        versioned_fs.switch_version(args.file_path, args.version)
    else:
        FUSE(VersionedFS(root), mountpoint, foreground=True, nonempty=True, direct_io=True)
