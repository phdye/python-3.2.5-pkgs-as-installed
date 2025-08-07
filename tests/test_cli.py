import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'site-packages'))
from sqlparse import cli


class CliTest(unittest.TestCase):

    def _run(self, argv):
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            cli.main(argv)
            return buf.getvalue()
        finally:
            sys.stdout = old

    def test_dump_config_cli(self):
        tmp = tempfile.mkdtemp()
        cfg = os.path.join(tmp, '.sqlparse')
        f = open(cfg, 'w')
        f.write('KeywordCase: Upper\n')
        f.close()
        sqlfile = os.path.join(tmp, 'a.sql')
        f = open(sqlfile, 'w')
        f.write('select 1;')
        f.close()
        out = self._run(['--dump-config', sqlfile])
        self.assertIn('KeywordCase: upper', out)

    def test_style_inline(self):
        tmp = tempfile.mkdtemp()
        sqlfile = os.path.join(tmp, 'b.sql')
        f = open(sqlfile, 'w')
        f.write('select 1;')
        f.close()
        out = self._run(['--style={IndentWidth: 9}', '--dump-config', sqlfile])
        self.assertIn('IndentWidth: 9', out)

    def test_style_name(self):
        tmp = tempfile.mkdtemp()
        sqlfile = os.path.join(tmp, 'd.sql')
        f = open(sqlfile, 'w')
        f.write('select 1;')
        f.close()
        out = self._run(['--style=mysql', '--dump-config', sqlfile])
        self.assertIn('KeywordCase: upper', out)

    def test_cli_overrides_config(self):
        tmp = tempfile.mkdtemp()
        cfg = os.path.join(tmp, '.sqlparse')
        f = open(cfg, 'w')
        f.write('KeywordCase: Lower\n')
        f.close()
        sqlfile = os.path.join(tmp, 'c.sql')
        f = open(sqlfile, 'w')
        f.write('select foo;')
        f.close()
        out = self._run(['--keywords', 'upper', sqlfile])
        self.assertIn('SELECT', out)


if __name__ == '__main__':
    unittest.main()

