<h1>FrittoMisto 🍟</h1>
<div style="margin-bottom: 200;">
<img src="docs/frittomisto.jpg" width="200" height="200" align="left"/>

<br>
Welcome to FrittoMisto, a Python module with a Fried Mix of utilities to enhance your day to day coding experience. 
<br>
<br>
Please note that FrittoMisto is currently at its very verge and not thoroughly tested. We invite you to explore, experiment, share your feedback or, even better, contribute! 👩‍🍳
</div>
<br>
<br>
<br>

## 🍤 Features / Philosophy

If you frequently develop Python tools, you might have experienced the repetition of using similar utilities or helpers across various applications. 
FrittoMisto was born out of my desire to consolidate these commonly used tools into a single swiss army knife. Now, I can effortlessly import and reuse them whenever necessary.

- **Mix of Utilities**: FrittoMisto serves up a diverse array of utilities, ranging from string manipulation to system interactions.

- **Simplicity**: Enjoy the simplicity and ease of use that FrittoMisto brings to your projects. FrittoMisto utilities are designed to be intuitive and require minimal code to achieve common tasks.

## 🍳 Installation

Install FrittoMisto using pip: `pip install frittomisto`

## 🍽️ Usage

Whet your appetite with a quick sample of FrittoMisto in action:

```python
from frittomisto.path import cd

with cd("/temporarily/move/here"):
  # do some stuff 
```

## 🍲 Documentation

### Path module

Utilities for paths and file system operations.

#### cd context manager

A context manager to temporarily move to a directory.

```python
from pathlib import Path
from frittomisto.path import cd

with cd("/path/to/dir"):
  print(Path.cwd()) # temporarely moved to "/path/to/dir"
```

#### sanitize_path

An utility to sanitize untrusted paths.

```python
from frittomisto.path import sanitize_path

# Throws a ValueError exception if path is not within allowed_dir 
sanitize_path("/path/to/dir", "/path/to/allowed/dir")

# Returns normalized absolude path if path is within allowed_dir
sanitize_path("/path/../to/dir", "/path/") # returns "/path/dir"
```

### Async module

Mix of asyncio utilities.

#### make_sync

A simple decorator to transform any async function into an sync function. 

```python
from frittomisto.asyncio import make_sync

@make_sync
async def an_async_function():
  ...

def a_sync_function():
  # The async function is now a sync function
  an_async_function()
```


### Profiling module


#### pp utils
The profiling module offers a set of simple functions to manage multiple 
perf counters:
- `pp_start(name)` starts a new counter named `name`
- `pp_stop(name)` stops the counter `name`
- `pp_get(name)` gets stat info of the counter `name`
- `pp_stats()` pretty print stats for all counters 

```python
from frittomisto.profiling import pp_start, pp_stop, pp_stats

pp_start("outer")
  for i in range(10):
    pp_start("func1")
    func1()
    pp_stop("func1")
    if i % 2 == 0:
      pp_start("func2")
      func2()
      pp_stop("func2")

pp_stop("outer")
pp_stats()

# This will show perf stats in a table format:
# PID    | Name  | tot_time           | rounds | avg_time            | max_time
# 169003 | outer | 5.679527849017177  | 1      | 5.679527849017177   | 5.679527849017177
# 169003 | func1 | 4.06138202897273   | 10     | 0.406138202897273   | 0.8546963339904323
# 169003 | func2 | 1.6178952640620992 | 5      | 0.32357905281241983 | 0.46843800198985264
```

### Config module

Utilities to manage your project configs.

#### cfg

The global instance of the program's config.

```python
import os
from pathlib import Path
from frittomisto.cfg import cfg
 with open(str(Path.cwd() / "frittomisto.toml"), "w", encoding="utf-8") as f:
  f.write(
    """
    [foo]
    bar = "hello"
    """
)

os.chdir("subdir") # configs are searched in all parent dirs
print(cfg["foo"]["bar"]) # prints hello
```

### IO module

#### no_print

Context manager to disable all calls to print

```python
from frittomisto.io import no_print

with no_print():
  print("hello") # does nothing
```

### Logging module

Logging utils.

#### get_logger
Get a named logger.

```python
from frittomisto.logging import get_logger

log = get_logger("my logger")
log.error("error message") # logs an error
```

#### log_level
Context manager to temporarily change log level.

```python
from frittomisto.logging import get_logger, log_level

with log_level("DEBUG"):
  log = get_logger("my logger")
  log.debug("debug message") # the debug message will be shown
```


## 👨‍🍳 Contributing

Craving more features or found a bug in our recipe? Contribute to FrittoMisto by opening an [issue](https://github.com/werew/frittomisto/issues) or submitting a [pull request](https://github.com/werew/frittomisto/pulls). 
Your contributions make the mix even more delightful!

## License

FrittoMisto is released under the [MIT License](https://opensource.org/licenses/MIT).

---
