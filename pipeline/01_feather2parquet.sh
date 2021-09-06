cd ../data/

cat << EOF > feather2parquet.py
#!/usr/bin/env python

import argparse
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    args = parser.parse_args()

    df = pd.read_feather(args.infile)
    pq.write_table(pa.Table.from_pandas(df), args.outfile)
    print(f"{args.infile} -> {args.outfile}")
EOF

python3 feather2parquet.py bPiofmZGb8o_csv_final.feather bPiofmZGb8o_csv_final.parquet
python3 feather2parquet.py wW1lY5jFNcQ_csv_final.feather wW1lY5jFNcQ_csv_final.parquet

aws s3 cp bPiofmZGb8o_csv_final.parquet s3://wxkzhe3i/data/
aws s3 cp wW1lY5jFNcQ_csv_final.parquet s3://wxkzhe3i/data/
rm feather2parquet.py
