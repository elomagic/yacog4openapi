# Yast Another Code Generator Tool 4 OpenAPI

Currently, prototype status

---

[![GitHub tag](https://img.shields.io/github/tag/elomagic/yacog4openapi.svg)](https://github.com/elomagic/yacog4openapi/tags/)
[![GitHub issues](https://img.shields.io/github/issues-raw/elomagic/yacog4openapi)](https://github.com/elomagic/yacog4openapi/issues)
[![Apache 2.0 license](https://img.shields.io/badge/Apache-2.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0-standalone.html)
[![made-with-micropython](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/elomagic/yacog4openapi/graphs/commit-activity)
[![Buymeacoffee](https://badgen.net/badge/icon/buymeacoffee?icon=buymeacoffee&label)](https://www.buymeacoffee.com/elomagic)

## Table of Contents

- [What about?](#what-about?)
- [Installation](#installation)
- [Configuration](#configuration)
- [Using](#using)
- [Contribution](#contribution)

# What About?

This project is currently a small prototype project how to read an Open API file and use a template engine in Python. 

# Installation

All required Python dependencies are declared in the *requirement.txt* file and must be installed with the following 
command by using the Python package manager *Pip*: 

```shell
pip install -r requirements.txt
```

# Configuration

```json5
{
    // Template to use
    "template": "resources/delphi-unit.jinja2",
    // File generated output
    "output": "..\\out\\uRestServiceClient.pas",
    // Open API datatype mappings
    "datatype-map": {
        "number,float":  "Single",
        "number,double": "Double",
        "number,": "Single",

        "integer,in32": "Integer",
        "integer,int64": "Int64",
        "integer,": "Integer",

        "string,byte": "String",
        "string,binary": "String",
        "string,": "String",

        "string,date": "TDate",
        "string,date-time": "TDateTime",

        "string,uuid": "String",

        "boolean,": "Boolean"
    }
}
```

tbc

# Using

**Example**
```shell
src/genclient.py --source=test/openapi.json --template=test/delphi-test.jinja2 --output=test-output/delphi-unit.pas
```

tbc

# Contribution

tbd