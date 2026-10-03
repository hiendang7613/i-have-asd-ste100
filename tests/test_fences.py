"""Code payloads are data, even when they look like reply instructions."""
import unittest
from test_check_reply import FULL
from check_reply import check, strip_code


class FenceTests(unittest.TestCase):
    def body_with(self, block):
        return FULL.replace('**Result-Zone**\n', '**Result-Zone**\n- **Example:** preserve this code:\n\n' + block + '\n\n')

    def test_tilde_and_long_backtick_fences_hide_payload_from_style_checks(self):
        payload = '**Agents-Zone**\n**Conclusion:** quoted data.\n- [raw] ☀\n' + 'word ' * 80
        for opening, closing in (('~~~text', '~~~'), ('````markdown', '````'), ('~~~', '~~~~~')):
            with self.subTest(opening=opening):
                reply = self.body_with(opening + '\n' + payload + '\n' + closing)
                report = check(reply)
                self.assertTrue(report['ok'], report)
                self.assertEqual(report['warnings'], [])

    def test_shorter_and_different_fences_do_not_close_the_block(self):
        block = '````markdown\n```\n**Conclusion:** quoted data.\n~~~\n- [raw] ☀\n````'
        self.assertTrue(check(self.body_with(block))['ok'])
        self.assertNotIn('quoted data', strip_code(block))

    def test_wrapped_sections_are_rejected_for_every_fence_style(self):
        for opening, closing in (('~~~markdown', '~~~'), ('````', '````'), ('```', '')):
            with self.subTest(opening=opening):
                reply = opening + '\n' + FULL + closing
                self.assertTrue(any('inside a code block' in text for text in check(reply)['violations']))

    def test_inline_backticks_are_not_a_fenced_block(self):
        self.assertEqual(strip_code('Use ``` as data on this line.'), 'Use ``` as data on this line.')


if __name__ == '__main__':
    unittest.main()
