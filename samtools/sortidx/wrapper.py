__author__ = "Kevin Murray"
__copyright__ = "Public Domain"
__email__ = "kdmfoss@gmail.com"
__license__ = "Unlicense"


from os import path
from snakemake.shell import shell

extra = snakemake.params.get("extra", "")
mem = snakemake.params.get("mem", "")
mem = "-m {}".format(mem) if mem else ""

outdir = path.basename(snakemake.output[0])
prefix = path.splitext(snakemake.output[0])[0]
tmpdir = path.join(snakemake.params.get("tmpdir", outdir), prefix)

shell(
    "(samtools sort"
    "   {extra}"
    "   -@ {snakemake.threads}"
    "   -o {snakemake.output[0]}"
    "   -T {tmpdir}"
    "   {snakemake.input[0]}"
    " && samtools index {snakemake.output[0]}"
    ") >{snakemake.log} 2>&1"
)
