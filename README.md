# archlinux-kali-tools
> Generate an install script for packages listed on kali.org/tools 
> which are available in the Arch Linux official repositories. 

## Overview
My goal here was to enable easy access to some common security tooling without 
needing to boot into a dedicated pentesting distribution. Most similar scripts 
I saw added the BlackArch repository (which I didn't want) and then just 
installed a static list of packages through `pacman`. Current availability is 
162 out of 677 tools, but many of the remaining tools are available through 
the AUR. 

## Usage
The only dependency is [requests](https://github.com/psf/requests). Install 
that, then run `python arch_kali_tools.py`. This will generate (3) files - 
`available`, `missing`, and `install.sh`. Execute `install.sh` to install 
available packages through `pacman`. 

Future runs will only query https://archlinux.org/packages/search/json/ if 
new packages are added to https://www.kali.org/tools (assuming you keep the
`available` and `missing` files intact).

There is lots of non-security software listed on that kali.org/tools page. You 
can specify an `ignored` file in the same directory as the script to exclude 
any packages that you don't want. Make sure you delete them from `available` 
if you've already generated that file.

## Example Output
```
$> python arch_kali_tools.py
[-] 0trace                         (1 of 677)
[-] aesfix                         (2 of 677)
[-] aeskeyfind                     (3 of 677)
[-] afflib                         (4 of 677)
[-] aflplusplus                    (5 of 677)
[+] aircrack-ng                    (6 of 677)
[-] airgeddon                      (7 of 677)
[-] altdns                         (8 of 677)
[-] amap                           (9 of 677)
[-] amass                          (10 of 677)
[-] android-sdk-meta               (11 of 677)
[-] apache-users                   (12 of 677)
[i] apache2                        (13 of 677)
[-] apktool                        (14 of 677)
[-] apple-bleee                    (15 of 677)
[-] arjun                          (16 of 677)
[-] armitage                       (17 of 677)
[+] arp-scan                       (18 of 677)
[-] arping                         (19 of 677)
[+] arpwatch                       (20 of 677)
```
* [+] indicates an available package
* [-] is missing
* [i] is explicitly ignored

## References
- https://wiki.archlinux.org/title/Official_repositories_web_interface
- https://www.kali.org/tools/

