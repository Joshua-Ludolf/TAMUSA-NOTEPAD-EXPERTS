<h1 align="center">Programming Languages Semester Project</h1> 
<br>
<p align="center">
<image  src="tne.png" alt="Jaguar Icon" class="center" ></image>
</p>

**Python Text Based Editor (Notepad)**

This project is a simple text-based editor implemented in Python. It consists of three main components for basic notepad functionality:

- **`notepad.py`**: This file contains the Notepad class that represents notepad application.
- **`file.py`**: This file handles file operations such as reading from and writing to files, ensuring that data is correctly managed and stored.
- **`execute.py`**: This file contains main function to initialize and run the NotePad application.
  
Other components:
- **`pyproject.toml`**: This file is used by the UV package manager, see additional features for documentation.
- **`tne.ico`**: This file is the icon for notepad application.
- **`tne.png`**: This file is the png file of icon for ReadMe documentation.
- **`emoji.py`**: This file contains EmojiPicker class that allows user to insert application builtin emojis.
- **`unittest.py`**: This file contains unit test for this application, primarily for basic utilization of this software.
  
The editor provides a basic interface for text manipulation, making it a useful tool for learning about file handling and user interface design in Python.
<br>

<h2 align="center"> The project employs a Functional/Object-Oriented programming approach to enhance code readability and maintainability. Key features include: </h2>

### Functional Programming Approach:

- **Pure Functions**: Functions are designed to avoid side effects, ensuring that they do not alter any state or data outside their scope.
- **Immutability**: Data structures are treated as immutable, reducing the likelihood of bugs caused by unintended modifications.
- **Higher-Order Functions**: Functions that take other functions as arguments or return them as results are used to create more flexible and reusable code.

### Object-Oriented Programming Approach:
- **Abstraction**: Abstraction in OOP allows the creation of simplified models of complex real-world entities by focusing on relevant attributes and behaviors while hiding unnecessary details. This makes the code easier to understand and maintain.
- **Encapsulation**: OOP bundles data and methods that operate on that data into objects. This encapsulation hides the internal state of objects and only exposes necessary functionalities, enhancing modularity and maintainability.
- **Inheritance**: OOP supports inheritance, allowing new classes to inherit properties and behaviors from existing classes. This promotes code reuse and can lead to a hierarchical class structure that simplifies the management of related objects.
- **Modularity and Reusability**: OOP promotes the creation of reusable and modular code. Classes and objects can be reused across different parts of the application or in different projects, reducing redundancy and improving consistency.

### Additional Features:

- **Emojis**: Based on Windows 11 builtin Emojis, allow for user expressions via visuals. In application, under Edit tab you'll find two options for inserting emojis, one less you manually pick from all emojis (`CTRL+E` also achieves this!) and the other is a reduced list from all types of emojis. 
- **Font Management**: `See FONT_FEATURES.md`
 - **UV Package Manager Support**: See documentation from developer of this amazing python package manager - <a href=https://docs.astral.sh/uv/>`https://docs.astral.sh/uv/.` </a>


## Quick Start

- **Windows (PowerShell):**

	```powershell
	# Using UV (no extra dependencies required)
	uv run .\execute.py

	# Or with Python directly
	python .\execute.py
	```

- **Linux/macOS (bash):**

	```bash
	# Using UV (no extra dependencies required)
	uv run ./execute.py

	# Or with Python directly
	python3 ./execute.py
	```

### Requirements

- Python 3.8+.
- Tkinter is part of the standard library on Windows and macOS. On Debian/Ubuntu you may need:

	```bash
	sudo apt-get update && sudo apt-get install -y python3-tk
	```

### Notes

- The project has no runtime PyPI dependencies; UV will start instantly without trying to install packages.
- If you prefer running tests:

	```bash
	# From the project root
	python -m unittest unit_tests.py
	```

## Docker

This project is a Tkinter GUI app. Containers can run it, but showing the window requires a working display server (X11/WSLg).

### Build (all platforms)

```bash
docker build -t tamusa-notepad:alpine .
```

### Run tests headlessly (all platforms)

Runs the unit tests under a virtual X server (Xvfb) inside the container:

```bash
docker run --rm tamusa-notepad:alpine xvfb-run python -m unittest unit_tests.py
```

### Windows users (recommended: run from WSL2 with WSLg)

Prerequisites:

- Windows 11 + WSL2.
- A WSL distro with WSLg enabled (GUI apps work inside WSL).

Sanity check (inside WSL):

```bash
sudo apt-get update
sudo apt-get install -y x11-apps
xeyes
```

If `xeyes` opens, you can run the Tkinter app container and show the window via WSLg.

Run the container (inside WSL):

```bash
docker run --rm \
	-e DISPLAY=$DISPLAY \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	joshludolf/tamusa-notepad:latest
```

Persist saved/created files to your project folder (inside WSL):

```bash
docker run --rm \
	-e DISPLAY=$DISPLAY \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-v "$(pwd)":/app \
	joshludolf/tamusa-notepad:latest
```

### Linux users (X11)

Allow local containers to connect to your X server (choose one):

```bash
xhost +local:
```

Run the GUI container:

```bash
docker run --rm \
	-e DISPLAY=$DISPLAY \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	joshludolf/tamusa-notepad:latest
```

Persist saved/created files to your current folder:

```bash
docker run --rm \
	-e DISPLAY=$DISPLAY \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-v "$(pwd)":/app \
	joshludolf/tamusa-notepad:latest
```



