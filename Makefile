# Bangladesh Food Price Watch. Use `make check` (stages.json vs disk markers, raw hashes, tests/).
# Heavy stages run in Colab (FoodPriceWatch_Colab.ipynb); `make stage` is the same logic from the command line.
PY ?= python
check:
	PYTHONPATH=src $(PY) -m fpw.check
.PHONY: check

# Run one stage like the Colab notebook does. Examples: make stage S=S01   make stage S=S06 DRY=1
stage:
	PYTHONPATH=src $(PY) -m fpw.runner $(S) $(if $(DRY),--dry,)
.PHONY: stage
