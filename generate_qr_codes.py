"""
GenQR - Styled QR Code Generator
---------------------------------
Interactively generates a QR code from plain text, a URL, contact info
(vCard), or Wi-Fi credentials. Outputs a styled PNG (custom module shapes,
solid/gradient colors, optional center logo) or a clean SVG.

Requirements:
    pip install "qrcode[pil]" --break-system-packages

Usage:
    python genqr.py
    (then just answer the prompts)
"""

import os
import sys

try:
    import qrcode
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import (
        SquareModuleDrawer,
        RoundedModuleDrawer,
        CircleModuleDrawer,
        GappedSquareModuleDrawer,
        VerticalBarsDrawer,
        HorizontalBarsDrawer,
    )
    from qrcode.image.styles.colormasks import (
        SolidFillColorMask,
        RadialGradiantColorMask,
        SquareGradiantColorMask,
        HorizontalGradiantColorMask,
        VerticalGradiantColorMask,
    )
except ImportError:
    print("Missing dependency. Install it first with:")
    print('    pip install "qrcode[pil]" --break-system-packages')
    sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def prompt_choice(prompt, options):
    """Show a numbered menu and return the chosen index (1-based)."""
    print(prompt)
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        choice = input("Enter choice number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        print("Invalid choice, try again.")


def hex_to_rgb(hex_color):
    hex_color = hex_color.strip().lstrip("#")
    if len(hex_color) != 6:
        return (0, 0, 0)
    try:
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return (0, 0, 0)


def get_hex_color(prompt_text, default):
    val = input(f"{prompt_text} (hex e.g. #1A1A1A, default {default}): ").strip()
    return val if val else default


# ---------------------------------------------------------------------------
# Content collection
# ---------------------------------------------------------------------------

def get_content():
    content_type = prompt_choice(
        "\nWhat do you want to encode?",
        ["Plain text", "URL", "Contact info (vCard)", "Wi-Fi credentials"],
    )

    if content_type == 1:
        data = input("Enter the text: ").strip()

    elif content_type == 2:
        url = input("Enter the URL: ").strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        data = url

    elif content_type == 3:
        print("\n--- Contact Details (leave blank to skip a field) ---")
        name = input("Full name: ").strip()
        org = input("Organization: ").strip()
        title = input("Job title: ").strip()
        phone = input("Phone number: ").strip()
        email = input("Email: ").strip()
        address = input("Address: ").strip()
        website = input("Website: ").strip()

        lines = ["BEGIN:VCARD", "VERSION:3.0", f"N:{name}", f"FN:{name}"]
        if org:
            lines.append(f"ORG:{org}")
        if title:
            lines.append(f"TITLE:{title}")
        if phone:
            lines.append(f"TEL;TYPE=CELL:{phone}")
        if email:
            lines.append(f"EMAIL:{email}")
        if address:
            lines.append(f"ADR:;;{address};;;;")
        if website:
            lines.append(f"URL:{website}")
        lines.append("END:VCARD")
        data = "\n".join(lines)

    else:  # Wi-Fi
        print("\n--- Wi-Fi Details ---")
        ssid = input("Network name (SSID): ").strip()
        password = input("Password (blank for open network): ").strip()
        enc = prompt_choice("Encryption type", ["WPA/WPA2", "WEP", "None (open)"])
        enc_str = {1: "WPA", 2: "WEP", 3: "nopass"}[enc]
        data = f"WIFI:T:{enc_str};S:{ssid};P:{password};;"

    return data


# ---------------------------------------------------------------------------
# Style collection (PNG only — SVG stays simple/vector-clean)
# ---------------------------------------------------------------------------

def get_style_options():
    print("\n--- Style Options ---")

    shape_choice = prompt_choice(
        "Module shape",
        [
            "Square (classic)",
            "Rounded",
            "Circle",
            "Gapped square",
            "Vertical bars",
            "Horizontal bars",
        ],
    )
    shape_map = {
        1: SquareModuleDrawer(),
        2: RoundedModuleDrawer(),
        3: CircleModuleDrawer(),
        4: GappedSquareModuleDrawer(),
        5: VerticalBarsDrawer(),
        6: HorizontalBarsDrawer(),
    }
    module_drawer = shape_map[shape_choice]

    color_choice = prompt_choice(
        "Color style",
        [
            "Solid color",
            "Radial gradient",
            "Square gradient",
            "Horizontal gradient",
            "Vertical gradient",
        ],
    )

    back_color = hex_to_rgb(get_hex_color("Background color", "#FFFFFF"))

    if color_choice == 1:
        fill_color = hex_to_rgb(get_hex_color("Fill color", "#000000"))
        color_mask = SolidFillColorMask(back_color=back_color, front_color=fill_color)
    else:
        color1 = hex_to_rgb(get_hex_color("Gradient color 1", "#000000"))
        color2 = hex_to_rgb(get_hex_color("Gradient color 2", "#4B0082"))

        if color_choice == 2:
            color_mask = RadialGradiantColorMask(
                back_color=back_color, center_color=color1, edge_color=color2
            )
        elif color_choice == 3:
            color_mask = SquareGradiantColorMask(
                back_color=back_color, center_color=color1, edge_color=color2
            )
        elif color_choice == 4:
            color_mask = HorizontalGradiantColorMask(
                back_color=back_color, left_color=color1, right_color=color2
            )
        else:
            color_mask = VerticalGradiantColorMask(
                back_color=back_color, top_color=color1, bottom_color=color2
            )

    logo_path = None
    if input("\nEmbed a logo image in the center? (y/N): ").strip().lower() == "y":
        path = input("Path to logo image file: ").strip()
        if os.path.isfile(path):
            logo_path = path
        else:
            print("File not found — continuing without a logo.")

    return module_drawer, color_mask, logo_path


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def generate_png(data, module_drawer, color_mask, logo_path, output_path, box_size, border):
    qr = qrcode.QRCode(
        error_correction=(
            qrcode.constants.ERROR_CORRECT_H if logo_path else qrcode.constants.ERROR_CORRECT_M
        ),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    kwargs = {"embeded_image_path": logo_path} if logo_path else {}

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=module_drawer,
        color_mask=color_mask,
        **kwargs,
    )
    img.save(output_path)


def generate_svg(data, output_path, box_size, border, fill_color, back_color):
    import qrcode.image.svg

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
        image_factory=qrcode.image.svg.SvgPathImage,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(output_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 50)
    print("  GenQR - Styled QR Code Generator")
    print("=" * 50)

    data = get_content()

    fmt_choice = prompt_choice(
        "\nOutput format",
        ["PNG (styled — shapes, colors, gradients, logo)", "SVG (clean vector)"],
    )

    box_size_in = input("\nBox size in pixels per module (default 10): ").strip()
    box_size = int(box_size_in) if box_size_in.isdigit() else 10

    border_in = input("Border thickness in modules (default 4): ").strip()
    border = int(border_in) if border_in.isdigit() else 4

    filename = input("\nOutput filename, no extension (default 'qrcode'): ").strip() or "qrcode"

    if fmt_choice == 1:
        module_drawer, color_mask, logo_path = get_style_options()
        output_path = f"{filename}.png"
        generate_png(data, module_drawer, color_mask, logo_path, output_path, box_size, border)
    else:
        fill_color = input("Fill color, name or hex (default 'black'): ").strip() or "black"
        back_color = input("Background color, name or hex (default 'white'): ").strip() or "white"
        output_path = f"{filename}.svg"
        generate_svg(data, output_path, box_size, border, fill_color, back_color)

    print(f"\n✅ QR code saved to: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main()