.. © 2017-2019, ETH Zurich, Institut für Theoretische Physik
.. Author: Dominik Gresch <greschd@gmx.ch>

.. _installation:

Installation
============

You can install ``aiida-tbmodels`` with

.. code:: bash

    python -m pip install aiida-tbmodels

where ``python`` is the interpreter for which you installed AiiDA.

To run TBmodels calculations, you will also have to set up the ``tbmodels`` CLI as an AiiDA code. After installing TBmodels, you can run ``which tbmodels`` to find the full path of the executable. Make sure to put ``unset PYTHONPATH`` into the prepend text of the code, since the ``PYTHONPATH`` set by AiiDA might interfere with your TBmodels installation.
