{
  description = "github-download-dependents-info downloads lists of dependents for GitHub repositories";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/23.11";
  };

  outputs = { self, nixpkgs }:
    let
      # Systems supported
      allSystems = [
        "x86_64-linux" # 64-bit Intel/AMD Linux
        "aarch64-linux" # 64-bit ARM Linux
        "x86_64-darwin" # 64-bit Intel macOS
        "aarch64-darwin" # 64-bit ARM macOS
      ];

      # Helper to provide system-specific attributes
      forAllSystems = f: nixpkgs.lib.genAttrs allSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      packages = forAllSystems ({ pkgs }:
        let
          pythonPackages = [
            pkgs.python311Packages.pip
            pkgs.python311Packages.requests
            pkgs.python311Packages.beautifulsoup4
          ];
          python = pkgs.python311.withPackages pythonPackages;
          app = python.pkgs.buildPythonApplication {
            name = "github-download-dependents-info";

            propagatedBuildInputs = pythonPackages;

            src = ./.;
          };
        in
        {
          default = app;
        });
    };
}
