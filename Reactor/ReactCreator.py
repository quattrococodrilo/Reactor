import shutil
import json
import os
import subprocess


class Reactor:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template = os.path.join(current_dir, "Template")
    package_conf = {
        "main": "index.js",
        "scripts": {
            "test": "echo \"Error: no test specified\" && exit 1",
            "build": "webpack --mode production",
            "start": "webpack-dev-server --open --mode development",
            "dev": "webpack serve --mode development --env development",
        },
        "keywords": [
            "react",
            "webpack"
        ],
        "husky": {
            "hooks": {
                "pre-commit": "lint-staged"
            }
        },
        "lint-staged": {
            "*.{js,jsx}": [
                "npm run lint",
                "git add"
            ]
        }
    }
    npm_modules = [
        "npm install react react-dom",
        "npm install webpack webpack-cli html-webpack-plugin\
            html-loader --save-dev",
        "npm install webpack-dev-server --save-dev",
        "npm install @babel/core babel-loader @babel/preset-env\
            @babel/preset-react --save-dev",
        "npm install mini-css-extract-plugin css-loader node-sass\
            sass-loader --save-dev",
        "npm install file-loader --save-dev",
        "npm install react-bootstrap bootstrap jquery @popperjs/core",
        "sudo npm install eslint babel-eslint eslint-config-airbnb\
            eslint-plugin-import eslint-plugin-react eslint-plugin-jsx-a11y",
    ]

    def __init__(self,
                 path_directory,
                 no_create_files=False,
                 no_install_npm=False):

        self.project = path_directory
        if self.project:
            not no_create_files and self.structure()
            not no_install_npm and self.npm_install()
        else:
            print("Enter a path and name project (my/project/path/name).")

    def structure(self):
        """ Copy Template to target directory. """
        shutil.copytree(self.template, self.project)

    def npm_install(self):
        """ Install NPM packages. """

        NPM_EXIST = subprocess.run(
            ["which", "npm"],
            capture_output=True
        ).stdout.decode(encoding="UTF-8")

        if NPM_EXIST:
            print("\n---------- NPM MODULES ----------")
            modules = self.npm_modules
            os.chdir(self.project)
            os.system("npm init -y")
            for module in modules:
                os.system(module)
                pass

            package_file = os.path.join("package.json")
            package_data = ""
            with open(package_file, "r") as f:
                package_data = json.loads(f.read())
            for key, value in self.package_conf.items():
                package_data[key] = value
            with open(package_file, "w") as f:
                f.write(json.dumps(package_data))
        else:
            print("NPM not found.")
