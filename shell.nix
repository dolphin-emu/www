{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = (with pkgs; [
    python312

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
  ]) ++ (with pkgs.python312Packages; [
    setuptools
    virtualenv
    pip
    Fabric
  ]);
}
