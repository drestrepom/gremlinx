# /path/to/my/project/makes/example/main.nix
{ inputs
, makePythonPypiEnvironment
, projectPath
, ...
}:
makePythonPypiEnvironment {
  name = "gremlinx";
  sourcesYaml = projectPath "/pypi-sources.yaml";
}
