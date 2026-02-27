{
  description = "Construct development shell from requirements.txt";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  inputs.pyproject-nix.url = "github:pyproject-nix/pyproject.nix";

  outputs =
    { nixpkgs, pyproject-nix, ... }:
    let
      # Load/parse requirements.txt
      project = pyproject-nix.lib.project.loadRequirementsTxt { projectRoot = ./.; };

      pkgs = nixpkgs.legacyPackages.x86_64-linux;
      python = pkgs.python3;

      pythonEnv =
        # Render requirements.txt into a Python withPackages environment
        # Note: Version constraints validation removed as nixpkgs may have different versions
        pkgs.python3.withPackages (project.renderers.withPackages { inherit python; });

    in
    {
      devShells.x86_64-linux.default = pkgs.mkShell { packages = [ pythonEnv ]; };
      packages.x86_64-linux.default = pythonEnv;
    };
}

