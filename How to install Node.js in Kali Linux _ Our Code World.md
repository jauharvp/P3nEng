

How to install Node.js in Kali Linux
====================================


**Warning Javascript Disabled:** Our Code World works better with
Javascript **

How to install Node.js in Kali Linux {.text-center}
------------------------------------


![How to install Node.js in Kali
Linux](How%20to%20install%20Node.js%20in%20Kali%20Linux%20|%20Our%20Code%20World_files/articleocw-58c522e4a3df0.jpg)

* * * * *

Obtaining software directly from the source code is a common procedure
on Unix computers, and generally involves the following three steps:
configuring the makefile, compiling the code, and finally installing the
executable to standard locations. In order to work with Node.js in Kali
Linux, it's recommendable to follow the mentioned process as it's easier
than other solutions.

Although Python is prefered when working with Kali Linux, both of the
programming languages (Python and JavaScript) have the same end goals.
There is no right or wrong decision for adopting which platform is best
suited to you, therefore if you want to work with JavaScript instead of
Python don't feel bad about that. Besides, Node can be utilized in the
broad range of modules, that means that you can use Python in your
Node.JS application and viceversa.

Let's get started with the installation !

#### Important

"Why should i create my own .deb of Node if i can download it from the
website ? ñee, what a stupid post ..." . As you know, Kali Linux is not
a normal Linux distribution, therefore the available package publicly in
the Node website may not work properly on it. You can try it it if you
want, but to guarantee a correct functionality, just follow these steps
and you should not have problems later.

1. Verify that you have all the required tools
----------------------------------------------

To create your own .deb package of Node, you will need python and the
compiler of c++ "g++". Execute the following command to install the
required tools (if they're already installed they should be only
updated):

``` {.language-bash .code-toolbar}
sudo apt-get install python g++ make checkinstall fakeroot Copy snippet
```

#### Note

You may get a warning like "dpkg was interrupted, you must manually run
'`sudo dpkg --configure -a`' to correct the problem". You just need, as
mentioned, execute `sudo dpkg --configure -a` to solve it and then
proceed with the command again.

2. Create a temporary folder
----------------------------

You should create a temporary folder to generate the .deb package of
Node.js. You can create it using mktemp, to make it with a single
command execute the following instruction:

``` {.language-bash .code-toolbar}
src=$(mktemp -d) && cd $src Copy snippet
```

The `-d` argument indicates that mktemp should make a directory instead
of a file. In this command we are creating a variable that contains the
generated temporary path by mktemp and then switching to that directory
in the terminal.

3. Download and extract Node.js
-------------------------------

Download the distributable code of Node.js executing the following
command in the terminal:

``` {.language-bash .code-toolbar}
wget -N http://nodejs.org/dist/node-latest.tar.gz Copy snippet
```

Once the download finishes, extract the content of the tar file with the
following command:

``` {.language-bash .code-toolbar}
tar xzvf node-latest.tar.gz && cd node-v* Copy snippet
```

This should create a folder with the preffix `node-v` that will vary
according to the downloaded version of Node.js.

4. Run configure script
-----------------------

A configure script is an executable script designed to aid in developing
a program to be run on a wide number of different computers. It matches
the libraries on the user's computer, with those required by the program
before compiling it from its source code. Run the configure script with
the following command:

``` {.language-bash .code-toolbar}
./configure Copy snippet
```

5. Create Node .deb package compiling the code
----------------------------------------------

To create our installable package of Node.js we are going to use
CheckInstall for it. CheckInstall keeps track of all the files created
or modified by your installation script and builds a standard binary
package (.deb, .rpm, .tgz). CheckInstall is really useful if you've got
a tarball with software that you have to compile (exactly what we're
doing in this moment).

To create the package of Node.js execute the following command:

``` {.language-bash .code-toolbar}
sudo fakeroot checkinstall -y --install=no --pkgversion $(echo $(pwd) | sed -n -re's/.+node-v(.+)$/\1/p') make -j$(($(nproc)+1)) install Copy snippet
```

Note that for most useful actions, checkinstall must be run as root.
We'll use fakeroot because as you may know, for security reason, it is a
good idea to avoid doing as root everything that could be done as normal
user, even if you can run sudo because it is your machine.

The command should start to compile Node.js and it will take a while, so
relax, get a cola and wait.

6. Install Node generated package
---------------------------------

Once the package is compiled, in the output of the previous step, you
should receive a message that specifies the name of the generated .deb
package:

![](How%20to%20install%20Node.js%20in%20Kali%20Linux%20|%20Our%20Code%20World_files/gallery-58c5bc257827c.jpg)

In this case, the name of our package is `node_7.7.2-1_amd64.deb`, now
we just need to install it using dpkg executing the following command:

#### Note

Remember to replace the value of the `i` argument with the name of the
generated package in the previous step.

``` {.language-bash .code-toolbar}
sudo dpkg -i [node generated package name.deb]
# Example: sudo dpkg -i node_7.7.2-1_amd64.deb Copy snippet
```

Wait till the installation finishes and that's it, you can now work with
Node.js in Kali Linux without problems. You can verify the version of
Node executing the following command in your terminal:

``` {.language-bash .code-toolbar}
node -v Copy snippet
```

Summary
-------

The next time that you want to install Node.js on your computer, just
execute the commands without following the entire tutorial:

``` {.language-bash .code-toolbar}
# Verify that you have all required tools
sudo apt-get install python g++ make checkinstall fakeroot
# Create tmp dir and switch to it
src=$(mktemp -d) && cd $src
# Download the latest version of Node
wget -N http://nodejs.org/dist/node-latest.tar.gz
# Extract the content of the tar file
tar xzvf node-latest.tar.gz && cd node-v*
# Run configuration
./configure
# Create .deb for Node
sudo fakeroot checkinstall -y --install=no --pkgversion $(echo $(pwd) | sed -n -re's/.+node-v(.+)$/\1/p') make -j$(($(nproc)+1)) install
# Replace [node_*] with the name of the generated .deb package of the previous step
sudo dpkg -i node_* Copy snippet
```

Happy coding **!

* * * * *
