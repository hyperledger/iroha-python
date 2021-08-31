# Iroha python

Python library for Hyperledger Iroha 2.

## Install

You should install rust (cargo) and python.

```sh
cargo build --release
cp target/release/libiroha2_sys.so iroha2/sys/iroha2.so
python3 test.py
```

## Architecture

### Stack

Architecturally python library uses rust client library. It is done
via wrapping classes using rust library [`pyo3`](pyo3.rs).

The data model of iroha itself is expected to be just classes without
some special methods (without sidechannels, like doing http request).
Communication channel for rust python methods using rust data model
is achieved using [`pythonize`](https://github.com/davidhewitt/pythonize)
rust library. It allows to represent almost all rust structures using
python objects (via serde serialization).

### Project layout

#### Python library

Python library right now is in [`iroha_python/iroha2`](iroha_python/iroha2). This directory has some 
directories:
- [`iroha2`](iroha_python/iroha2) -- iroha2 library itself. Contains client and key generation at root
- [`iroha2.crypto`](iroha_python/iroha2/crypto) -- iroha crypto bindings
- [`iroha2.data_model`](iroha_python/iroha2/data_model) -- data model with all instructions, queries and expressions
- [`iroha2.sys`](iroha_python/iroha2/sys) -- raw bindings to rust structures wrapped around python objects

#### Rust code

- [`iroha_python`](iroha_python) is rust sys library (sys in terms of raw bindings without abstractions)
- [`iroha_python/generate`](iroha_python/generate) is used for generating classes for rust structures

## Generating python sys sources

There is a need to regenerate sys sources and update client library after major rust updates in data model.

```sh
cd generate
cargo run ../iroha2/sys
```

