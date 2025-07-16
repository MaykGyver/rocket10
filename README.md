# 🚀 Rocket 10

A minimalist Windows 10 remix that launches your perfect system from *PowerShell* and *winget*.

## Usage

1. Get a windows installation iso of your choice. (Windows 10 IoT Enterprise LTSC for best results)
2. Create a USB installation medium using [Rufus](https://rufus.ie) or a comparable software product (If you want or need a virtual medium, create and attach a vhdx using Windows' disk manager. Rufus will recognize and write to it.)
3. Run 🚀 Rocket 10
   ```bash
   winget install Git.Git  # if you ain't got the git client yet
   git clone https://github.com/MaykGyver/rocket10.git; cd rocket10  # get and enter the 🚀 Rocket 10 experience
   winget install Python.Python.3.13  # if you ain't got a recent python yet
   pip install pipenv  # if your python ain't got pipenv yet
   pipenv update  # sets up the python virtual environment for rocket10.py from Pipfile
   pipenv run python rocket10.py  # executes 🚀 Rocket 10 in its virtual environment; modifies installation medium from step 2 for step 4
   ```
4. Use installation medium on new device.
5. Await updates.
6. Use *PowerShell* and *winget* on the new device to configure the exact system you need.
