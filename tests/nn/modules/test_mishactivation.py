# MishActivation

import torch
from zeta.nn import MishActivation
from torch import nn
from packaging import version


def test_MishActivation_init():
    mish_activation = MishActivation()

    if version.parse(torch.__version__) < version.parse("1.9.0"):
        assert mish_activation.act == mish_activation._mish_python
    else:
        assert mish_activation.act == nn.functional.mish


def test__mish_python():
    mish_activation = MishActivation()
    input = torch.tensor([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
    expected_output = input * torch.tanh(nn.functional.softplus(input))

    assert torch.equal(mish_activation._mish_python(input), expected_output)


def test_forward():
    mish_activation = MishActivation()
    input = torch.tensor([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])

    if version.parse(torch.__version__) < version.parse("1.9.0"):
        expected_output = input * torch.tanh(nn.functional.softplus(input))
    else:
        expected_output = nn.functional.mish(input)

    assert torch.equal(mish_activation.forward(input), expected_output)
