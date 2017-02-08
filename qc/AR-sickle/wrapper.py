# Copyright (c) 2017 Kevin Murray <kdmfoss@gmail.com>
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from uuid import uuid1 as uuid
from snakemake.shell import shell

phred_enc_in = snakemake.params.get('phred_enc_in', '33')
uncompress_prog = snakemake.params.get('uncompress_prog', 'zcat')
compress_prog = snakemake.params.get('compress_prog', 'gzip')
tmpdir = snakemake.params.get('tmpdir', '/tmp')
minqual = snakemake.params.get('minimum_quality', '20')
minlen = snakemake.params.get('minimum_length', '50')
tag = str(uuid())

log = snakemake.log_fmt_shell()

shell(
    "(( {uncompress_prog} {snakemake.input}"
    " | seqhax pairs"
    "   -f"
    "   -p {tmpdir}/{tag}_paired.fastq"
    "   -u {tmpdir}/{tag}_unpaired.fastq"
    "   -"
    " ) && AdapterRemoval"
    "   --file1 {tmpdir}/{tag}_paired.fastq"
    "   --output1 {tmpdir}/{tag}_paired_AR.fastq"
    "   --interleaved"
    "   --qualitybase {phred_enc_in}"
    "   --qualitybase-output 33" # always output in sanger fmt
    "   --combined-output"
    "   --collapse"
    "   --settings {tmpdir}/{tag}_ar_report.txt"
    " && cat {tmpdir}/{tag}_ar_report.txt"  # output to log file
    " && ( cat "
    "   {tmpdir}/{tag}_paired_AR.fastq"
    "   {tmpdir}/{tag}_unpaired.fastq"
    " | sickle se"
    "   -f /dev/stdin"
    "   -q {minqual}"
    "   -t sanger"
    "   -l {minlen}"
    "   -o >({compress_prog} > {snakemake.output.reads})"
    " ) && rm -rf {tmpdir}/{tag}*"
    ") {log}"
)
