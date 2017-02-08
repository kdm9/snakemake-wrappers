__author__ = "Kevin Murray"
__copyright__ = "Public Domain"
__email__ = "kdmfoss@gmail.com"
__license__ = "Unlicense"


from os import path
from snakemake.shell import shell

extra = snakemake.params.get("extra", "")
compressor = snakemake.params.get("compressor", "gzip")
log = snakemake.log_fmt_shell()

shell(
    "(fastq-dump"
    "   --split-spot"
    "   --skip-technical"
    "   --stdout"
    "   --readids"
    "   --defline-seq '@$sn/$ri'"
    "   --defline-qual '+'"
    "   {extra}"
    "   {snakemake.input}"
    "| {compressor} > {snakemake.output}"
    ") {log}"
)
