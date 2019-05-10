# Copyright (C) 2018-2019 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

# ===============================================================================
# Generated file for Model Optimizer Operation extension for a layer
#
# You need to modify this file if you need to
#   1. set default values for several attributes of the layer
#      (do it in __init__() method)
#   2. lessen number of attributes to appear in the IR
#      (specify such a list in backend_attrs() method)
#   3. handle the layer which output blob is different to the input one
#      (implement your own static method infer() and set it as attribute in
#      __init__() dictionary)
#
# Refer to the section "Extending Model Optimizer with New Primitives" in
# OpenVINO* documentation (either online or offline in
# <INSTALL_DIR>/deployment_tools/documentation/docs/index.html an then navigate
# to the corresponding section).
# ===============================================================================



from mo.ops.op import Op
from mo.front.common.partial_infer.elemental import copy_shape_infer
from mo.graph.graph import Node


class coshOp(Op):
    op = 'Cosh'
    
    def __init__(self, graph, attrs):
        mandatory_props = dict(
            type=__class__.op,
            op=__class__.op,
            
            infer=coshOp.infer            
        )
        super().__init__(graph, mandatory_props, attrs)
    
    
    
    
    @staticmethod
    def infer(node: Node):
        # ==========================================================
        # You should add your shape calculation implementation here
        # If a layer input shape is different to the output one
        # it means that it changes shape and you need to implement
        # it on your own. Otherwise, use copy_shape_infer(node).
        # ==========================================================
        return copy_shape_infer(node)


