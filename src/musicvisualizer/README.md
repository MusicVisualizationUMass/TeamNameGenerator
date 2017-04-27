# MusicVisualizer by TeamNameGenerator --- Source Directory

## The Source Tree

Broadly speaking, the project is broken into two main sections: the Pipeline and
the UI. These can be accessed via their respective directories.

## Tests

The `unittest` framework is used. From this directory (i.e., `/src/`) the
`unittest` framework can be called as follows:

    python3.5 -m unittest path/to/test

For example, to test the `ir.py` file, run

    python3 -m unittest pipeline/test/test_ir.py

