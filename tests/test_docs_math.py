"""Regression checks for the site's Markdown math configuration."""
import unittest
from pathlib import Path

import markdown
from mkdocs.config import load_config

ROOT = Path(__file__).resolve().parents[1]


class MathRenderingTests(unittest.TestCase):
    def render(self, text):
        config = load_config(str(ROOT / 'mkdocs.yml'))
        return markdown.markdown(text, extensions=config['markdown_extensions'],
                                 extension_configs=config['mdx_configs'])

    def test_math_fence_preserves_tex(self):
        tex = r'\mathcal{L}_{IS} = \frac{\pi_{\theta}(a_t)}{\pi_{old}(a_t)}'
        html = self.render('```math\n' + tex + '\n```')
        self.assertIn('class="arithmatex"', html)
        self.assertIn(tex, html)
        self.assertNotIn('<code', html)
        self.assertNotIn('<pre', html)

    def test_existing_math_delimiters(self):
        html = self.render(r'$x_t$ and \(y_t\)' + '\n\n$$\nz_t^2\n$$')
        self.assertEqual(html.count('class="arithmatex"'), 3)
        self.assertNotIn('<em>', html)

    def test_code_is_not_math(self):
        html = self.render('```python\nx_t = "$value$"\n```')
        self.assertIn('<code', html)
        self.assertNotIn('class="arithmatex"', html)

    def test_every_staged_math_fence(self):
        import re
        count = 0
        for page in (ROOT / '.docs').rglob('*.md'):
            source = page.read_text()
            fences = len(re.findall(r'^```math\s*$', source, re.MULTILINE))
            if fences:
                html = self.render(source)
                self.assertNotIn('language-math', html, str(page))
                self.assertGreaterEqual(html.count('class="arithmatex"'), fences, str(page))
                count += fences
        self.assertGreater(count, 0)
        print(f'Checked {count} math fences across staged documentation')


if __name__ == '__main__':
    unittest.main()
