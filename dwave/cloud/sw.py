"""
Interface to software :term:`sampler`s available through the D-Wave API.

Software samplers have the same interface (response) as QPU samplers, with
classical software resources generating samples.
"""

from __future__ import absolute_import

from dwave.cloud.client import Client as BaseClient
from dwave.cloud.solver import Solver
from dwave.cloud.computation import Future

__all__ = ['Client']


class Client(BaseClient):
    """D-Wave API client specialized to work with remote software solvers
    (samplers).

    This class is instantiated by default, or explicitly when `client=sw`, with the
    typical base client instantiation :code:`with Client.from_config() as client:` of
    a client.

    Examples:
        This example indirectly instantiates a :class:`dwave.cloud.sw.client` based
        on the local system`s default D-Wave Cloud Client configuration file to sample
        a random Ising problem tailored to fit the client`s default solver`s graph.

        .. code-block:: python

            import random
            from dwave.cloud import Client

            # Use context manager to ensure resources (thread pools used by Client) are released
            with Client.from_config(client='sw') as client:

                solver = client.get_solver()

                # Build problem to exactly fit the solver graph
                linear = {index: random.choice([-1, 1]) for index in solver.nodes}
                quad = {key: random.choice([-1, 1]) for key in solver.undirected_edges}

                # Sample 100 times and print out the first sample
                computation = solver.sample_ising(linear, quad, num_reads=100)
                print(computation.samples[0])

    """

    @staticmethod
    def is_solver_handled(solver):
        """Determine if the specified solver should be handled by this client.

        This predicate function overrides superclass to allow only remote software solvers.

        Current implementation allows only D-Wave software clients with solver IDs
        prefixed with `c4-sw`. If needed, update this method to suit your solver
        naming scheme.

        Examples:
            This example filters solvers for those prefixed My_SW_Solver.

            .. code:: python

                @staticmethod
                def is_solver_handled(solver):
                    if not solver:
                        return False
                    return solver.id.startswith('My_SW_Solver')

        """
        if not solver:
            return False
        return solver.id.startswith('c4-sw_')
