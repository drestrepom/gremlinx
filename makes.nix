{
  lintPython = {
    dirsOfModules = {
      makes = {
        python = "3.8";
        src = "/gremlinx/";
      };
    };
    modules = {
      principal = {
        python = "3.8";
        src = "/gremlinx/";
      };
    };
  };
  formatPython = {
    enable = true;
    targets = [
      "/" # Entire project
    ];
  };
  formatMarkdown = {
    enable = true;
    doctocArgs = [ "--title" "# Contents" ];
    targets = [ "/README.md" ];
  };
  lintMarkdown = {
    all = {
      targets = [ "/" ];
    };
  };
}
