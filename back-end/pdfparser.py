import pymupdf


def extract_text(file_path: str) -> str:
    """
    Extract text from a research paper PDF.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Extracted text from the PDF.
    """

    document = pymupdf.open(file_path)
    pages = []

    for page in document:
        blocks = page.get_text("blocks")

        blocks = sorted(
            blocks,
            key=lambda block: (block[1], block[0])
        )

        page_text = []

        for block in blocks:
            text = block[4].strip()

            if text:
                page_text.append(text)

        if page_text:
            pages.append("\n\n".join(page_text))

    document.close()

    return "\n\n".join(pages)