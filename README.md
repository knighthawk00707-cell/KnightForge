# KnightForge

**Professional Password Wordlist Generator**

KnightForge is a desktop application for generating customized password wordlists from user-provided base strings, numbers, substitutions, symbols, case variations, placement rules, and password filters.

Built with **Python** and **PySide6**, KnightForge provides a graphical interface for creating, previewing, filtering, saving, loading, and exporting generated password lists.

> **Project status:** Working desktop application — v1.0

---

## Features

### Password Generation

* Generate password variations from custom base strings
* Lowercase, uppercase, capitalization, and alternate-case variations
* Numeric combinations and ranges
* Zero-padded numbers
* Number permutations
* Ascending and configurable number ordering
* Symbol combinations
* Character substitution rules
* Number placement rules
* Password length filtering
* Duplicate handling
* Result sorting
* Generation estimation

### Project Management

* Create a new project
* Save project settings
* Load previously saved projects
* Project files use the `.kfproj` format
* Settings are maintained through a centralized application state

### User Interface

* PySide6 desktop interface
* Dashboard
* Base Data page
* Rules page
* Preview page
* Export page
* Settings page
* Sidebar navigation
* Toolbar actions
* Keyboard shortcuts
* Application icon/logo

### Export

Generated passwords can be exported from the application for use in authorized password-auditing and security-testing workflows.

---

## Screenshots

Add screenshots of KnightForge here as the project develops.

Example:

```markdown
![KnightForge Dashboard](resources/screenshots/dashboard.png)
```

Recommended screenshots:

* Dashboard
* Base Data
* Rules
* Password Preview
* Export
* Settings

---

## Requirements

For running KnightForge from source:

* Python 3.10+
* PySide6

The project may also be distributed as a standalone executable using PyInstaller.

---

## Installation From Source

Clone the repository:

```bash
git clone https://github.com/knighthawk00707-cell/KnightForge.git
cd KnightForge
```

Create a virtual environment:

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run KnightForge:

```bash
python main.py
```

---

## Building a Standalone Application

KnightForge can be packaged with PyInstaller.

Install PyInstaller:

```bash
pip install pyinstaller
```

### Linux

```bash
python -m PyInstaller --windowed --name KnightForge main.py
```

The application will be created under:

```text
dist/KnightForge/
```

Run it with:

```bash
./dist/KnightForge/KnightForge
```

### Windows

Build KnightForge on a Windows system:

```powershell
python -m PyInstaller --windowed --name KnightForge main.py
```

The executable will be located under:

```text
dist/KnightForge/
```

### macOS

Build KnightForge on macOS:

```bash
python3 -m PyInstaller --windowed --name KnightForge main.py
```

The generated application will be placed under:

```text
dist/
```

> PyInstaller builds are platform-specific. Build the application separately on Linux, Windows, and macOS.

---

## Project Structure

```text
KnightForge/
│
├── knightforge.py
│
├── controllers/
│   ├── project_controller.py
│   └── profiles_controller.py
│
├── engine/
│   ├── filter.py
│   ├── generator.py
│   ├── numbers.py
│   ├── placement.py
│   ├── rules.py
│   ├── strings.py
│   ├── substitutions.py
│   └── symbols.py
│
├── gui/
│   ├── main_window.py
│   ├── pages/
│   └── widgets/
│
├── models/
│   ├── app_state.py
│   └── settings.py
│
├── workers/
│   └── generation_worker.py
│
├── resources/
│   └── icons/
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Project Files

KnightForge projects can be saved using:

```text
.kfproj
```

Project files contain generator settings such as:

* Base strings
* Number configuration
* Symbol configuration
* Substitution rules
* Placement rules
* Password length settings
* Generation options

Do not place sensitive information into project files that you do not want stored or shared.

---

## Security

KnightForge is designed as a **local desktop application**.

Generated passwords and wordlists are processed locally by the application. The project does not require an online service for password generation.

However, users should still treat generated wordlists and project files as potentially sensitive data.

### Important recommendations

* Do not commit real passwords to Git.
* Do not commit private wordlists containing sensitive information.
* Do not upload `.kfproj` files containing sensitive data.
* Do not include generated password lists in public repositories.
* Keep sensitive project files outside the Git repository.
* Review generated files before sharing them.

KnightForge should be used only for systems, accounts, networks, and security assessments that you are authorized to test.

---

## Responsible Use

KnightForge is intended for legitimate purposes including:

* Security research
* Authorized password auditing
* Penetration testing
* Security education
* Password policy testing
* Controlled laboratory environments
* Recovery of authorized test data

Do not use KnightForge to attack accounts, systems, or services without authorization.

The developers are not responsible for misuse of this software.

---

## Development

Clone the repository and install the development dependencies:

```bash
git clone https://github.com/knighthawk00707-cell/KnightForge.git
cd KnightForge
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

When making changes, test the application from source before creating a PyInstaller build.

---

## Contributing

Contributions are welcome.

Before submitting a pull request:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test the application.
5. Commit your changes.
6. Push the branch.
7. Open a pull request.

Example:

```bash
git checkout -b feature/my-improvement
```

Keep pull requests focused and avoid unrelated changes.

---

## Bug Reports

If you find a bug, open an issue and include:

* Operating system
* Python version
* KnightForge version
* Steps to reproduce the problem
* Expected behavior
* Actual behavior
* Relevant error messages or traceback

Do not include passwords, private wordlists, credentials, or other sensitive information in bug reports.

---

## Roadmap

Future improvements may include:

* Improved installers for Windows, Linux, and macOS
* Automated release builds
* Code signing
* Additional export formats
* Improved project management
* More extensive automated testing
* Performance improvements
* UI improvements

The core goal is to keep KnightForge stable and reliable while improving its usability.

---

## License

KnightForge is released under the **MIT License**.

See [`LICENSE`](LICENSE) for the full license text.

---

## Disclaimer

KnightForge is provided for legitimate security testing, research, education, and authorized password-auditing purposes.

Users are responsible for ensuring that their use of the software complies with applicable laws, regulations, policies, and authorization requirements.

---

## Author

**KnightForge Contributors**

Built with:

* Python
* PySide6
* PyInstaller

---

⭐ If KnightForge is useful to you, consider starring the repository.
