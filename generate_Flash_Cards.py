"""
GenFlashcard - Convert Notes into Printable Flashcards
--------------------------------------------------------
Takes your notes (typed in, pasted, or loaded from a .txt file) and turns
them into a printable, cut-and-fold flashcard deck as a PDF, a CSV
(importable into Anki/Quizlet), or both.

Requirements:
    pip install reportlab --break-system-packages

Usage:
    python genflashcard.py
    (then answer the prompts)

Supported note formats (auto-detected):
    Q: What is the capital of France?
    A: Paris

    Q: ...
    A: ...

    --- or ---

    Mitochondria :: Powerhouse of the cell
    Photosynthesis :: Process plants use to convert light to energy

    --- or ---

    Term - Definition
    Term - Definition

    --- or ---

    (plain alternating lines: question line, then answer line, repeat)
"""

import csv
import os
import re
import sys

try:
    from reportlab.lib.pagesizes import A4, LETTER
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
except ImportError:
    print("Missing dependency. Install it first with:")
    print("    pip install reportlab --break-system-packages")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def prompt_choice(prompt, options):
    print(prompt)
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        choice = input("Enter choice number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        print("Invalid choice, try again.")


def read_multiline(instructions):
    """Read multiple lines from the terminal until the user types a lone
    'END' on its own line."""
    print(instructions)
    print("(type END on its own line when you're done)\n")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Parsing notes into (question, answer) pairs
# ---------------------------------------------------------------------------

def parse_notes(raw_text):
    text = raw_text.strip()
    if not text:
        return []

    lines = [l for l in text.split("\n")]

    # Format 1: Q:/A: blocks
    if re.search(r"^\s*Q\s*[:.]", text, re.IGNORECASE | re.MULTILINE):
        return _parse_qa_blocks(lines)

    # Format 2: "::" delimiter
    if any("::" in l for l in lines if l.strip()):
        return _parse_delimited(lines, "::")

    # Format 3: " - " delimiter
    if any(re.search(r"\s-\s", l) for l in lines if l.strip()):
        return _parse_delimited_regex(lines, r"\s-\s")

    # Format 4: "|" delimiter
    if any("|" in l for l in lines if l.strip()):
        return _parse_delimited(lines, "|")

    # Fallback: alternating non-empty lines = question, answer
    non_empty = [l.strip() for l in lines if l.strip()]
    pairs = []
    for i in range(0, len(non_empty) - 1, 2):
        pairs.append((non_empty[i], non_empty[i + 1]))
    return pairs


def _parse_qa_blocks(lines):
    pairs = []
    question, answer = None, None
    for line in lines:
        stripped = line.strip()
        q_match = re.match(r"^Q\s*[:.]\s*(.*)", stripped, re.IGNORECASE)
        a_match = re.match(r"^A\s*[:.]\s*(.*)", stripped, re.IGNORECASE)
        if q_match:
            if question is not None and answer is not None:
                pairs.append((question, answer))
                question, answer = None, None
            question = q_match.group(1).strip()
        elif a_match:
            answer = a_match.group(1).strip()
        elif stripped and question is not None and answer is None:
            question += " " + stripped
        elif stripped and answer is not None:
            answer += " " + stripped
    if question is not None and answer is not None:
        pairs.append((question, answer))
    return pairs


def _parse_delimited(lines, delimiter):
    pairs = []
    for line in lines:
        if delimiter in line:
            parts = line.split(delimiter, 1)
            q, a = parts[0].strip(), parts[1].strip()
            if q and a:
                pairs.append((q, a))
    return pairs


def _parse_delimited_regex(lines, pattern):
    pairs = []
    for line in lines:
        if not line.strip():
            continue
        parts = re.split(pattern, line, maxsplit=1)
        if len(parts) == 2:
            q, a = parts[0].strip(), parts[1].strip()
            if q and a:
                pairs.append((q, a))
    return pairs


# ---------------------------------------------------------------------------
# Content collection
# ---------------------------------------------------------------------------

def get_flashcards():
    mode = prompt_choice(
        "\nHow do you want to provide your notes?",
        [
            "Type/paste notes now (Q:/A:, 'term :: definition', 'term - definition', or plain alternating lines)",
            "Enter flashcards one at a time (guided prompts)",
            "Load notes from a .txt file",
        ],
    )

    if mode == 1:
        raw = read_multiline("\nPaste or type your notes below.")
        cards = parse_notes(raw)

    elif mode == 2:
        cards = []
        print("\nEnter each flashcard. Leave the question blank to finish.\n")
        while True:
            q = input(f"Card {len(cards) + 1} - Question: ").strip()
            if not q:
                break
            a = input(f"Card {len(cards) + 1} - Answer: ").strip()
            cards.append((q, a))

    else:
        path = input("\nPath to .txt file: ").strip()
        if not os.path.isfile(path):
            print("File not found.")
            return []
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        cards = parse_notes(raw)

    if not cards:
        print("\nNo flashcards were parsed. Check your formatting and try again.")
    else:
        print(f"\nParsed {len(cards)} flashcard(s).")
        preview = input("Show a preview before generating output? (y/N): ").strip().lower()
        if preview == "y":
            for i, (q, a) in enumerate(cards, 1):
                print(f"  {i}. Q: {q}")
                print(f"     A: {a}")

    return cards


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------

def export_csv(cards, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Question", "Answer"])
        for q, a in cards:
            writer.writerow([q, a])


# ---------------------------------------------------------------------------
# PDF export (printable, cut-and-fold grid, duplex-aligned front/back)
# ---------------------------------------------------------------------------

def wrap_text(c, text, font_name, font_size, max_width):
    """Basic word-wrap for a canvas, returns a list of lines."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if c.stringWidth(trial, font_name, font_size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_card(c, x, y, width, height, text, label, font_size=13):
    """Draw one card's border (dashed cut line) and centered wrapped text."""
    c.saveState()
    c.setDash(4, 3)
    c.setLineWidth(0.75)
    c.rect(x, y, width, height)
    c.setDash()

    c.setFont("Helvetica", 7)
    c.setFillGray(0.55)
    c.drawString(x + 5, y + height - 11, label)
    c.setFillGray(0)

    padding = 14
    max_width = width - 2 * padding
    font_name = "Helvetica-Bold" if label == "Q" else "Helvetica"

    fs = font_size
    lines = wrap_text(c, text, font_name, fs, max_width)
    # shrink font until the text block fits vertically, down to a floor
    while len(lines) * (fs + 3) > (height - 2 * padding) and fs > 7:
        fs -= 1
        lines = wrap_text(c, text, font_name, fs, max_width)

    c.setFont(font_name, fs)
    line_height = fs + 3
    total_text_height = len(lines) * line_height
    start_y = y + (height + total_text_height) / 2 - fs

    for line in lines:
        text_width = c.stringWidth(line, font_name, fs)
        tx = x + (width - text_width) / 2
        c.drawString(tx, start_y, line)
        start_y -= line_height

    c.restoreState()


def generate_pdf(cards, output_path, page_size_name, mirror_for_duplex):
    page_size = A4 if page_size_name == "A4" else LETTER
    page_width, page_height = page_size

    card_width = 3.3 * inch
    card_height = 2.1 * inch
    margin = 0.4 * inch
    gutter = 0.15 * inch

    cols = max(1, int((page_width - 2 * margin + gutter) // (card_width + gutter)))
    rows = max(1, int((page_height - 2 * margin + gutter) // (card_height + gutter)))
    per_page = cols * rows

    grid_w = cols * card_width + (cols - 1) * gutter
    grid_h = rows * card_height + (rows - 1) * gutter
    start_x = (page_width - grid_w) / 2
    start_y = page_height - (page_height - grid_h) / 2 - card_height

    c = canvas.Canvas(output_path, pagesize=page_size)

    chunks = [cards[i:i + per_page] for i in range(0, len(cards), per_page)]

    for chunk in chunks:
        # ---- FRONT PAGE (questions) ----
        for idx, (q, a) in enumerate(chunk):
            row, col = divmod(idx, cols)
            x = start_x + col * (card_width + gutter)
            y = start_y - row * (card_height + gutter)
            draw_card(c, x, y, card_width, card_height, q, "Q")
        c.showPage()

        # ---- BACK PAGE (answers, mirrored for duplex alignment) ----
        for idx, (q, a) in enumerate(chunk):
            row, col = divmod(idx, cols)
            if mirror_for_duplex:
                col = cols - 1 - col
            x = start_x + col * (card_width + gutter)
            y = start_y - row * (card_height + gutter)
            draw_card(c, x, y, card_width, card_height, a, "A")
        c.showPage()

    c.save()
    return len(chunks) * 2, cols, rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 55)
    print("  GenFlashcard - Notes to Printable Flashcards")
    print("=" * 55)

    cards = get_flashcards()
    if not cards:
        return

    filename = input("\nOutput filename, no extension (default 'flashcards'): ").strip() or "flashcards"

    fmt_choice = prompt_choice(
        "\nOutput format",
        ["PDF (printable, cut-and-fold deck)", "CSV (for Anki/Quizlet import)", "Both PDF and CSV"],
    )

    if fmt_choice in (2, 3):
        csv_path = f"{filename}.csv"
        export_csv(cards, csv_path)
        print(f"CSV saved to: {os.path.abspath(csv_path)}")

    if fmt_choice in (1, 3):
        page_choice = prompt_choice("\nPage size", ["A4", "Letter"])
        page_size_name = "A4" if page_choice == 1 else "Letter"

        duplex_choice = input(
            "\nWill you print double-sided (flip on long edge)? (Y/n): "
        ).strip().lower()
        mirror_for_duplex = duplex_choice != "n"

        pdf_path = f"{filename}.pdf"
        num_pages, cols, rows = generate_pdf(cards, pdf_path, page_size_name, mirror_for_duplex)
        print(
            f"PDF saved to: {os.path.abspath(pdf_path)}  "
            f"({num_pages} pages, {cols}x{rows} cards/page, {len(cards)} cards total)"
        )
        if mirror_for_duplex:
            print("Tip: print double-sided, flipping on the LONG edge, then cut along the dashed lines.")
        else:
            print("Tip: print fronts, reload the same pages, then print backs; then cut along the dashed lines.")


if __name__ == "__main__":
    main()