{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = (with pkgs; [
    python39Full

    gettext
    transifex-client

    # CPython extension common build deps.
    git
    openssl
    libjpeg
    pkg-config
    stdenv
    zlib
    postgresql
    libffi
  ]) ++ (with pkgs.python39Packages; [
    setuptools
    virtualenv
    pip
    Fabric
  ]);
}
