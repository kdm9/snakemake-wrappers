__author__ = "Johannes Köster"
__copyright__ = "Copyright 2016, Johannes Köster"
__email__ = "koester@jimmy.harvard.edu"
__license__ = "MIT"


from snakemake.shell import shell

extra = snakemake.params.get('extra', '')
rgid = snakemake.params.get('rgid', '')
if rgid:
    rgsamp = snakemake.params.get('rgsample', rgid)
    rgid = "-R '@RG\\tID:{}\\tSM:{}'".format(rgid, rgsamp

shell(
    "(bwa mem"
    "   {extra} {rgid}"
    "   -t {snakemake.threads}"
    "   {snakemake.input.ref}"
    "   {snakemake.input.sample}"
    "| samtools view"
    "   -Sbh"
    "   -o {snakemake.output[0]}"
    "   - "
    ") >{snakemake.log} 2>&1"
)
