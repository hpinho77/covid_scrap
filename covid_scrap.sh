#!/bin/bash
source /Users/hugo/miniconda2/etc/profile.d/conda.sh
conda activate covid
cd /Users/hugo/PycharmProjects/COVID
#python /Users/hugo/PycharmProjects/COVID/covid_scrap.py 2>&1 | tee /Users/hugo/PycharmProjects/COVID/covid_scrap.log 
python /Users/hugo/PycharmProjects/COVID/covid_scrap.py
