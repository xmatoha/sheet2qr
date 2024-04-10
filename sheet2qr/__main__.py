import click
from sheet2qr import sheet2qr
import reportlab.lib.pagesizes as ps


default_config = {
    "num_rows": 7,
    "num_cols": 5,
    "margin": 10,
    "page_size": ps.A4,
}


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = default_config


@cli.group("from-xlsx")
@click.option("--file")
@click.option("--sheet-name")
@click.pass_context
def from_xlsx(ctx, file, sheet_name):
    ctx.obj["src_file"] = file
    ctx.obj["sheet_name"] = sheet_name
    ctx.obj["src_file_type"] = "xlsx"


@from_xlsx.command("to-pdf")
@click.option("--file")
@click.pass_context
def to_pdf(ctx, file):
    ctx.obj["dst_file"] = file
    ctx.obj["dst_file_type"] = "pdf"
    sheet2qr(ctx.obj)


if __name__ == "__main__":
    cli()
