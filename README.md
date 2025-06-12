<h1 align="center">Programming Languages Semester Project</h1> 
<br>
<p align="center">
<image  src="tne.png" alt="Jaguar Icon" class="center" ></image>
</p>

**Python Text Based Editor (Notepad)**

This project is a simple text-based editor implemented in Python. It consists of three main components for basic notepad functionality:

- **notepad.py**: This file contains the Notepad class that represents notepad application.
- **file.py**: This file handles file operations such as reading from and writing to files, ensuring that data is correctly managed and stored.
- **execute.py**: This file contains main function to initialize and run the NotePad application.
  
Other components:
- **pyproject.toml**: This file is used by the UV package manager, see additional features for documentation.
- **tne.ico**: This file is the icon for notepad application.
- **tne.png**: This file is the png file of icon for ReadMe documentation.
- **emoji.py**: This file contains EmojiPicker class that allows user to insert application builtin emojis.
- **unittest.py**: This file contains unit test for this application, primarily for basic utilization of this software.
  
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

- **UV Package Manager Support**: See documentation from developer of this amazing python package manager - https://astral.sh/blog/uv.
- **Emojis**: Based on Windows 11 builtin Emojis, allow for user expressions via visuals.
