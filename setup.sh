#!/bin/bash
export base_dir=$(pwd)
originalfile="snakemake_config.yaml"
tmpfile=$(mktemp)
cp --attributes-only --preserve $originalfile $tmpfile
cat $originalfile | envsubst > $tmpfile && mv $tmpfile $originalfile