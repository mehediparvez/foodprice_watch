# Bangladesh Food Price Watch. Use `make check` (stages.json vs disk markers, raw hashes, tests/).
# Stages run from the Colab notebook (FoodPriceWatch_Colab.ipynb); there is no local `make stage` target.
PY ?= python
check:
	PYTHONPATH=src $(PY) -m fpw.check
.PHONY: check
