{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = (with pkgs; [
    python39Full

    # CPython extension common build deps.
    git
    openssl
    libjpeg
    pkg-config
    stdenv
    zlib
    postgresql
  ]) ++ (with pkgs.python39Packages; [
    setuptools
    virtualenv
    pip
    Fabric
  ]);
}
