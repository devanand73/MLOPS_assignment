# Find commit hash
dvc list . --rev HEAD~5

# Restore specific version
dvc checkout data/processed.dvc --rev a1b2c3d
git commit -am "Rollback to data version a1b2c3d"