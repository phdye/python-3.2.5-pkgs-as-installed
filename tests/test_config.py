import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'site-packages'))
from sqlparse import config


class ConfigFileTest(unittest.TestCase):

    def test_parse_simple_values(self):
        text = 'KeywordCase: Upper\nStripComments: yes\nIndentWidth: 4\n'
        opts = config.load_from_string(text)
        self.assertEqual(opts['keyword_case'], 'upper')
        self.assertTrue(opts['strip_comments'])
        self.assertEqual(opts['indent_width'], 4)

    def test_based_on_style(self):
        text = 'BasedOnStyle: mysql\nKeywordCase: Lower\n'
        opts = config.load_from_string(text)
        # mysql style sets keyword_case upper, overridden by Lower
        self.assertEqual(opts['keyword_case'], 'lower')

    def test_find_config_upwards(self):
        tmp = tempfile.mkdtemp()
        root_cfg = os.path.join(tmp, '.sqlparse')
        f = open(root_cfg, 'w')
        f.write('KeywordCase: Upper\n')
        f.close()
        sub = os.path.join(tmp, 'sub')
        os.mkdir(sub)
        inner_cfg = os.path.join(sub, '.sqlparse')
        f = open(inner_cfg, 'w')
        f.write('KeywordCase: Lower\n')
        f.close()
        file_path = os.path.join(sub, 'x.sql')
        f = open(file_path, 'w')
        f.write('select 1')
        f.close()
        cfg = config.load_config(file_path)
        self.assertEqual(cfg['keyword_case'], 'lower')
        cfg_parent = config.load_config(tmp)
        self.assertEqual(cfg_parent['keyword_case'], 'upper')

    def test_load_style_inline(self):
        style = config.load_style('{IndentWidth: 6}')
        self.assertEqual(style['indent_width'], 6)

    def test_unknown_style(self):
        self.assertRaises(ValueError, config.load_style, 'mystyle')

    def test_dump_config(self):
        opts = config.DEFAULT_CONFIG.copy()
        opts['indent_width'] = 7
        dumped = config.dump_config(opts)
        self.assertIn('IndentWidth: 7', dumped)


if __name__ == '__main__':
    unittest.main()

