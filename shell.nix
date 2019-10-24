{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = (with pkgs; [
    python37Full

    # CPython extension common build deps.
    git
    openssl
    libjpeg
    pkgconfig
    stdenv
    zlib
    postgresql
  ]) ++ (with pkgs.python37Packages; [
    setuptools
    virtualenv
    pip
    Fabric
  ]);
}
