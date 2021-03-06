# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import os
import os.path
import zipfile

import qiime.sdk


def get_dummy_plugin():
    plugin_manager = qiime.sdk.PluginManager()
    if 'dummy-plugin' not in plugin_manager.plugins:
        raise RuntimeError(
            "When running QIIME 2 unit tests, the QIIMETEST environment "
            "variable must be defined so that plugins required by unit tests "
            "are loaded. The value of the QIIMETEST environment variable can "
            "be anything. Example command: QIIMETEST=1 nosetests")
    return plugin_manager.plugins['dummy-plugin']


class ArchiveTestingMixin:
    """Mixin for testing properties of archives created by Archiver."""

    def assertArchiveMembers(self, archive_filepath, root_dir, expected):
        """Assert members are in an archive.

        Parameters
        ----------
        archive_filepath : str
            Filepath to archive whose members will be verified against the
            `expected` members.
        root_dir : str
            Root directory of the archive. Will be prepended to the member
            paths in `expected`. This is useful when the archive's root
            directory is not known ahead of time (e.g. when it is a random
            UUID) and the caller is determining the root directory dynamically.
        expected : set of str
            Set of expected archive members stored as paths relative to
            `root_dir`.

        """
        with zipfile.ZipFile(archive_filepath, mode='r') as zf:
            observed = set(zf.namelist())

        # Path separator '/' is hardcoded because paths in the zipfile will
        # always use this separator.
        expected = {root_dir + '/' + member for member in expected}

        self.assertEqual(observed, expected)

    def assertExtractedArchiveMembers(self, extract_dir, root_dir, expected):
        """Assert an archive's members are extracted to a directory.

        Parameters
        ----------
        extract_dir : str
            Path to directory the archive was extracted to.
        root_dir : str
            Root directory of the archive that was extracted to `extract_dir`.
            This is useful when the archive's root directory is not known ahead
            of time (e.g. when it is a random UUID) and the caller is
            determining the root directory dynamically.
        expected : set of str
            Set of expected archive members extracted to `extract_dir`. Stored
            as paths relative to `root_dir`.

        """
        observed = set()
        for root, _, filenames in os.walk(extract_dir):
            for filename in filenames:
                observed.add(os.path.join(root, filename))

        expected = {os.path.join(extract_dir, root_dir, member)
                    for member in expected}

        self.assertEqual(observed, expected)
