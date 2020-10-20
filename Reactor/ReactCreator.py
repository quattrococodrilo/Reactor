# import argparse
import json
import os
import subprocess
from urllib import request


class Reactor:

    scripts = {
        "test": "echo \"Error: no test specified\" && exit 1",
        "build": "webpack --mode production",
        "start": "webpack-dev-server --open --mode development",
    }

    npm_modules = [
        "npm install react react-dom",
        "npm install @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev",
        "npm install webpack webpack-cli html-webpack-plugin html-loader --save-dev",
        "npm install webpack-dev-server --save-dev",
        "npm install file-loader --save-dev",
        "npm install mini-css-extract-plugin css-loader node-sass sass-loader --save-dev",
        "sudo npm install eslint babel-eslint eslint-config-airbnb eslint-plugin-import eslint-plugin-react eslint-plugin-jsx-a11y",
    ]

    def __init__(self,
                 path_directory,
                 verbose=False,
                 no_create_files=False,
                 no_install_npm=False):

        self._verbose = verbose
        self._no_install_npm = no_install_npm
        self._no_create_files = no_create_files
        self._project = path_directory
        if self._project:
            not no_create_files and self.structure()
            not no_install_npm and self.npm_install()
        else:
            print("Enter a path and name project (my/project/path/name).")

    def structure(self):
        """ Return a list of files to be created.
        Each item must be: {'path': 'path/to/file', 'url': 'url/to/download/file'}  """

        src = os.path.join(self._project, "src")
        not os.path.isdir(src) and os.makedirs(src)
        components = os.path.join(src, "components")
        not os.path.isdir(components) and os.makedirs(components)
        assets = os.path.join(src, "assets")
        not os.path.isdir(assets) and os.makedirs(assets)
        styles = os.path.join(assets, "styles")
        not os.path.isdir(styles) and os.makedirs(styles)
        static = os.path.join(assets, "static")
        not os.path.isdir(static) and os.makedirs(static)
        public = os.path.join(self._project, "public")
        not os.path.isdir(public) and os.makedirs(public)

        files = [
            {
                "path": os.path.join(src, "index.js"),
                "url":  "https://raw.githubusercontent.com/quattrococodrilo/CodeNotes/main/React/Template/src/index.js"
            },
            {
                "path": os.path.join(public, "index.html"),
                "url": "https://raw.githubusercontent.com/quattrococodrilo/CodeNotes/main/React/Template/public/index.html"
            },
            {
                "path": os.path.join(self._project, ".babelrc"),
                "url": "https://github.com/quattrococodrilo/CodeNotes/blob/main/React/Template/.babelrc"
            },
            {
                "path": os.path.join(self._project, "webpack.config.js"),
                "url": "https://raw.githubusercontent.com/quattrococodrilo/CodeNotes/main/React/Template/webpack.config.js"
            },
            {
                "path": os.path.join(self._project, ".eslintrc"),
                "url": "https://raw.githubusercontent.com/quattrococodrilo/CodeNotes/main/React/Template/.eslintrc"
            },
            {
                "path": os.path.join(self._project, ".gitignore"),
                "url": "https://raw.githubusercontent.com/quattrococodrilo/CodeNotes/main/React/Template/.gitignore"
            }
        ]

        for f_data in files:
            with open(f_data["path"], "w") as f:
                if "url" in f_data and f_data["url"]:
                    req = request.Request(f_data["url"])
                    with request.urlopen(req) as response:
                        f.write(response.read().decode(encoding="UTF-8"))
                else:
                    f.write("")
            if self._verbose:
                print(f_data["path"])
                print("------------------------------")

    def npm_install(self):
        """ Install NPM packages. """

        NPM_EXIST = subprocess.run(
            ["which", "npm"],
            capture_output=True
        ).stdout.decode(encoding="UTF-8")

        if NPM_EXIST:
            print("\n---------- NPM MODULES ----------")
            modules = self.npm_modules
            os.chdir(self._project)
            os.system("npm init -y")
            for module in modules:
                os.system(module)
                pass

            package_file = os.path.join("package.json")
            package_data = ""
            with open(package_file, "r") as f:
                package_data = json.loads(f.read())
            package_data["scripts"] = self.scripts
            with open(package_file, "w") as f:
                f.write(json.dumps(package_data))
        else:
            print("NPM not found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates a React project."
    )
    parser.add_argument("-p", "--path", required=True,
                        help="path/to/directory")
    parser.add_argument("-nm", "--no_install_modules", action="store_true",
                        help="no install modules")
    parser.add_argument("-nf", "--no_create_files", action="store_true",
                        help="no create files")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="show output files creation")
    args = parser.parse_args()

    Reactor(
        path_directory=args.path,
        verbose=args.verbose,
        no_create_files=args.no_create_files,
        no_install_npm=args.no_install_modules
    )
