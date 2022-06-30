# Github Download Dependents Info

Download a repo's "Used by" page as a CSV

## Usage

```
pip install bs4 requests
python dl-dependency.py <USER>/<repo>
```

## Example

```
python dl-dependency.py fastai/nbdev
```

```python
>>> import pandas as pd
pd.read_csv("repo_dependency.csv").sort_values(by=["stars", "forks"], ascending=False)

                     repo_name  stars  forks
661            fastai/fastbook  15207   5601
673    ml-tooling/ml-workspace   2607    350
613                lvwerra/trl    439     59
624     nikitakaraevv/pointnet    160     50
134         MannLabs/alphapept    109     22
..                         ...    ...    ...
668  joheras/decoFungiNotebook      0      0
669     jctc-sol/docker_images      0      0
672        ncoop57/nb_template      0      0
674     yamaton/advent-of-code      0      0
675  cimarieta/nlp-b2w-reviews      0      0

[676 rows x 3 columns]
```
## TODO
- [ ] Get it to work on `django/django` as a benchmark.
