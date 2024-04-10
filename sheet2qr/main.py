import qrcode
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from io import BytesIO
from reportlab.pdfgen import canvas
from sheet2dict import Worksheet


def sheet_to_dict_list(ws):
    ret = []
    for v in ws.sheet_items:
        d = {key: v[key]
             for key in ws.header}
        ret.append(d)
    return ret


def format_dict(dict):
    return '\n'.join(
        [f"{key} = {value}" for key, value in dict.items()])


def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_buff = BytesIO()
    img.save(img_buff, format="PNG")
    return img_buff


def sheet_factory(sheet_type, file_name, sheet_name=None):
    if sheet_type == "xlsx":
        if sheet_name is not None:
            return Worksheet().xlsx_to_dict(path=file_name, select_sheet=sheet_name)
        else:
            return Worksheet().xlsx_to_dict(path=file_name)
    elif sheet_type == "csv":
        ws = Worksheet()
        with open(file_name, "r") as f:
            ws.csv_to_dict(csv_file=f, delimiter=';')
            return ws
    else:
        raise Exception(f"Unsupported sheet format {sheet_type}")


def sheet2qr(config):
    qr_codes = []
    ws = sheet_factory(config["src_file_type"],
                       config["src_file"], config.get("sheet_name"))
    list_dict = sheet_to_dict_list(ws)
    for d in list_dict:

        qr_codes.append(ImageReader(generate_qr(format_dict(d))))
    generate_pdf(
        config["dst_file"],
        config["num_rows"],
        config["num_cols"],
        config["margin"],
        config["page_size"],
        qr_codes,
    )


def generate_pdf(output_file, num_rows, num_cols, margin, page_size, images):
    page_width, page_height = page_size
    margin = margin * mm
    cell_width = (page_width - 2 * margin) / num_cols
    cell_height = (page_height - 2 * margin) / num_rows

    chunk_size = num_rows * num_cols
    pages = [images[i:i + chunk_size]
             for i in range(0, len(images), chunk_size)]
    c = canvas.Canvas(output_file, pagesize=page_size)
    for s in pages:
        # Place images in the grid
        for index, image_path in enumerate(s):
            row = index // num_cols
            col = index % num_cols

            x = margin + col * cell_width
            # Coordinates start from the bottom-left
            y = page_height - margin - (row + 1) * cell_height

            # Draw the image in the specified grid cell
            c.drawImage(image_path, x, y, width=cell_width,
                        height=cell_height, preserveAspectRatio=True)

        for row in range(num_rows + 1):
            start_x = margin
            end_x = page_width - margin
            y = page_height - margin - row * cell_height
            c.line(start_x, y, end_x, y)

        for col in range(num_cols + 1):
            x = margin + col * cell_width
            start_y = margin
            end_y = page_height - margin
            c.line(x, start_y, x, end_y)
        # Save the PDF
        c.showPage()
    c.save()
