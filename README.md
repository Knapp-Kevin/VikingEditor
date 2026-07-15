# Valheim Editor (.fch)

An interactive, desktop-based GUI tool written in Python and PySide6 to safely decompile, edit, sign, and recompile Valheim character save files (`.fch`). 

No more dealing with complex hex editors or worrying about breaking your character's save file signature. This tool parses the binary structures of your Viking's inventory, skills, appearance, and stats, letting you make changes through an intuitive visual interface.

## Table of Contents
- [Features](#features)
- [Installation & Setup](#installation--setup)
- [How to Use](#how-to-use)
- [How to find your `.fch` files](#how-to-find-your-fch-files)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)

## Features

- **Inventory Tab**: Edit item IDs, stack counts, and durability.
- **Skills Tab**: View and easily adjust skill levels (from Run to Axes) using simple sliders or numerical inputs.
- **Stats Tab**: Edit player health, stamina, and key game progression stats.
- **Appearance Tab**: Visually customize skin tone and hair/beard color with integrated color pickers, and toggle models/styles.
- **Misc Tab (Rename Character)**: Safely change your character's name in the `.fch` outer container. Saving automatically suggests a file name that matches Valheim's standard (`lowercase_name.fch`).
- **Signature Protection**: Automatically calculates SHA-512 hashes and re-signs files during compilation so Valheim accepts the edited saves without throwing corruption errors.

## Installation & Setup

### Prerequisites
Make sure you have **Python 3.9+** installed on your system.

### 1. Clone the Repository

```bash
git clone [https://github.com/miskamero/ValheimEditor.git](https://github.com/miskamero/ValheimEditor.git)
cd ValheimEditor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the application:

```bash
python main.py
```

## How to Use

1. Launch the application.
2. Open a `.fch` file using the "Open" button. (See [How to find your `.fch` files](#how-to-find-your-fch-files) below for guidance.)
3. Navigate through the tabs to edit your character's inventory, skills, stats, and appearance.
4. After making changes, click "Save" to compile and sign the edited `.fch` file. The application will suggest a filename based on your character's name, but you can choose a different name if desired.
5. Place the newly saved `.fch` file back into your Valheim save directory and launch the game to see your changes.

## How to find your `.fch` files

You should move your saves from Cloud to Local in Valheim's main menu. Then, you can find your `.fch` files in the following directory:

`%username%\AppData\LocalLow\IronGate\Valheim`

#### **⚠️ CRITICAL SAFETY WARNING: Always make a backup copy of your .fch files before editing them! Put your backup in a safe folder OUTSIDE of the Valheim save directory. If you lose your save or corrupt it by accident, you will not be able to recover it.**

## Project Structure

```
├── main.py                     # Application entry point
├── ui/
│   ├── mainWindow.py           # Main Qt window & save controller
│   ├── inventoryTab.py         # Inventory grid/table editor
│   ├── skillsTab.py            # Skill level sliders
│   ├── statsTab.py             # Health & Stamina configurations
│   ├── appearanceTab.py        # Colors & styling customizer
│   └── miscTab.py              # Name and filename synchronizer
└── subscripts/
    ├── fchUtil.py              # Wrapper unpacker & SHA-512 signer
    └── playerDataUtil.py       # Inner binary decoder & packing pipeline
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue on the GitHub repository. Please remember that I am only one person, so I may not be able to respond to every request or suggestion. If you want to contribute, please make sure your code is well-documented and follows the existing style.

## Disclaimer

This is an unofficial, community-made tool. It is not affiliated with, authorized, or endorsed by Iron Gate Studio or Coffee Stain Publishing. Always back up your saves!
