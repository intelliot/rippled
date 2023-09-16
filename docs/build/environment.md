Our [build instructions][BUILD.md] assume you have a C++ development
environment complete with Git, Python, Conan, CMake, and a C++ compiler.
This document exists to help readers set one up on any of the Big Three
platforms: Linux, macOS, or Windows.

[BUILD.md]: ../../BUILD.md


## Linux

Package ecosystems vary across Linux distributions,
so there is no one set of instructions that will work for every Linux user.
These instructions are written for Ubuntu 22.04.
They are largely copied from the [script][1] used to configure our Docker
container for continuous integration.
That script handles many more responsibilities.
These instructions are just the bare minimum to build one configuration of
rippled.
You can check that codebase for other Linux distributions and versions.
If you cannot find yours there,
then we hope that these instructions can at least guide you in the right
direction.

```
apt update
apt install --yes curl git libssl-dev python3.10-dev python3-pip make g++-11

curl --location --remote-name \
  "https://github.com/Kitware/CMake/releases/download/v3.25.1/cmake-3.25.1.tar.gz"
tar -xzf cmake-3.25.1.tar.gz
rm cmake-3.25.1.tar.gz
cd cmake-3.25.1
./bootstrap --parallel=$(nproc)
make --jobs $(nproc)
make install
cd ..

pip3 install 'conan<2'
```

[1]: https://github.com/thejohnfreeman/rippled-docker/blob/master/ubuntu-22.04/install.sh


## macOS

Open a Terminal and enter the below command to bring up a dialog to install
the command line developer tools.
Once it is finished, this command should return a version greater than the
minimum required (see [BUILD.md][]).

```
clang --version
```

The command line developer tools should include Git too:

```
git --version
```

Install [Homebrew][],
use it to install [pyenv][],
use it to install Python,
and use it to install Conan:

[Homebrew]: https://brew.sh/
[pyenv]: https://github.com/pyenv/pyenv

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew update
brew install xz
brew install pyenv
pyenv install 3.10-dev
pyenv global 3.10-dev
eval "$(pyenv init -)"
pip install 'conan<2'
```

Install CMake with Homebrew too:

```
brew install cmake
```


## Windows

There are various ways to set up a C++ development environment on
Windows. One approach is to use the [Windows Subsystem for Linux
(WSL)](https://docs.microsoft.com/en-us/windows/wsl/), which simplifies
many of the Linux-based tasks on Windows.

### Windows Subsystem for Linux (WSL)

1. Install [WSL](https://docs.microsoft.com/en-us/windows/wsl/install).
   You can use WSL 2 for better performance.
   
2. Once installed, choose the Ubuntu distribution from the Microsoft
   Store.

3. After installing Ubuntu, open the Ubuntu terminal. Follow the Linux
   instructions above.

### Git and C++

1. Download and install [Git for
   Windows](https://git-scm.com/download/win). This will allow you to
   use Git from the command prompt or PowerShell.

2. For C++ development on Windows, consider [Visual
   Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
   During installation, select the “Desktop development with C++”
   workload.

It should be possible to build this project with Visual Studio 2019.

### Python, Conan, CMake

1. Download and install [Python for
   Windows](https://www.python.org/downloads/windows/). Ensure that you
   add Python to the system PATH during installation.

2. Open a command prompt or PowerShell terminal.

3. Install Conan using pip:
   ```
   pip install 'conan<2'
   ```

4. Download and install [CMake for
   Windows](https://cmake.org/download/). Make sure to add CMake to the
   system PATH during installation.

With a working C++ development environment on Windows, you can follow
the build instructions in [BUILD.md](../../BUILD.md).
