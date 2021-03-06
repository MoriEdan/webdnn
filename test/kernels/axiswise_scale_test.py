import numpy as np

from test.util import generate_kernel_test_case
from webdnn.graph.axis import Axis
from webdnn.graph.graph import Graph
from webdnn.graph.operators.axiswise_scale import AxiswiseScale
from webdnn.graph.order import OrderC, OrderNHWC, OrderCNHW, OrderNCHW
from webdnn.graph.variable import Variable
from webdnn.graph.variables.constant_variable import ConstantVariable


def test_minor_axis():
    vx = np.random.rand(10, 6, 4, 8)
    vs = np.random.rand(8)
    vy = vx * vs[None, None, None, :]

    x = Variable(vx.shape, order=OrderNHWC)
    s = ConstantVariable(vs, order=OrderC)
    y, = AxiswiseScale(None, axis=Axis.C)(x, s)

    generate_kernel_test_case(
        description=f"AxiswiseScale for minor axis",
        backend=["webgpu", "webassembly", "fallback"],
        graph=Graph([x], [y]),
        inputs={x: vx},
        expected={y: vy}
    )


def test_middle_axis():
    vx = np.random.rand(10, 6, 4, 8)
    vs = np.random.rand(6)
    vy = vx * vs[None, :, None, None]

    x = Variable(vx.shape, order=OrderNCHW)
    s = ConstantVariable(vs, order=OrderC)
    y, = AxiswiseScale(None, axis=Axis.C)(x, s)

    generate_kernel_test_case(
        description=f"AxiswiseScale for middle axis",
        backend=["webgpu", "fallback"],
        graph=Graph([x], [y]),
        inputs={x: vx},
        expected={y: vy}
    )


def test_major_axis():
    vx = np.random.rand(10, 6, 4, 8)
    vs = np.random.rand(10)
    vy = vx * vs[:, None, None, None]

    x = Variable(vx.shape, order=OrderCNHW)
    s = ConstantVariable(vs, order=OrderC)
    y, = AxiswiseScale(None, axis=Axis.C)(x, s)

    generate_kernel_test_case(
        description=f"AxiswiseScale for major axis",
        backend=["webgpu", "fallback"],
        graph=Graph([x], [y]),
        inputs={x: vx},
        expected={y: vy}
    )


def test_mix_order():
    vx = np.random.rand(10, 6, 4, 8)
    vs = np.random.rand(10)
    vy = vx * vs[:, None, None, None]

    x = Variable(vx.shape, order=OrderCNHW)
    s = ConstantVariable(vs, order=OrderC)
    y, = AxiswiseScale(None, axis=Axis.C)(x, s)

    x.change_order(OrderNHWC)
    vx = np.rollaxis(vx, 0, 4)

    generate_kernel_test_case(
        description=f"AxiswiseScale for mix order",
        backend=["webgpu"],
        graph=Graph([x], [y]),
        inputs={x: vx},
        expected={y: vy}
    )
