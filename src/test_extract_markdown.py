import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links

class TestMarkdownExtract(unittest.TestCase):
    def test_images_basic(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_links_basic(self):
        text = (
            "This is text with a link [to boot dev](https://www.boot.dev) and "
            "[to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_images_and_links_mixed(self):
        text = (
            "Mix ![img1](http://ex.com/1.png) and [site](http://ex.com) "
            "and ![img2](http://ex.com/2.jpg)"
        )
        self.assertEqual(
            extract_markdown_images(text),
            [("img1", "http://ex.com/1.png"), ("img2", "http://ex.com/2.jpg")],
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("site", "http://ex.com")],
        )

    def test_no_matches(self):
        self.assertEqual(extract_markdown_images("no images here"), [])
        self.assertEqual(extract_markdown_links("no links here"), [])

    def test_ignores_image_as_link(self):
        text = "![alt](http://ex.com/x.png)"
        self.assertEqual(extract_markdown_links(text), [])

if __name__ == "__main__":
    unittest.main()
