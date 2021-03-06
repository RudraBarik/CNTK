# Copyright (c) Microsoft. All rights reserved.

# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

import os
import re
import sys
import pytest

abs_path = os.path.dirname(os.path.abspath(__file__))
notebook = os.path.join(abs_path, "..", "..", "..", "..", "Tutorials", "CNTK_205_Artistic_Style_Transfer.ipynb")

linux_only = pytest.mark.skipif(sys.platform == 'win32', reason="temporarily disable these two tests on Windows due to an issue introduced by adding onnx to our CI.")
@linux_only
def test_cntk_205_artistic_style_transfer_noErrors(nb):
    if os.getenv("OS")=="Windows_NT" and sys.version_info[0] == 2:
        pytest.skip('tests with Python 2.7 on Windows are not stable in the CI environment. ')
    errors = [output for cell in nb.cells if 'outputs' in cell
              for output in cell['outputs'] if output.output_type == "error"]
    assert errors == []

expected_objective = 316284.22
relative_tolerance = 1e-1 # would be tighter if specific to python 2 vs. 3

@linux_only
def test_cntk_205_artistic_style_transfer_evalCorrect(nb):
    if os.getenv("OS")=="Windows_NT" and sys.version_info[0] == 2:
        pytest.skip('tests with Python 2.7 on Windows are not stable in the CI environment. ')
    testCell = [cell for cell in nb.cells
                if cell.cell_type == 'code' and re.search('objfun.xstar', cell.source)]
    assert len(testCell) == 1
    actual_objective = float(testCell[0].outputs[0]['data']['text/plain'])
    assert abs((actual_objective-expected_objective)/expected_objective) < relative_tolerance
