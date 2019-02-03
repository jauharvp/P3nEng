Our Code World uses cookies to ensure you get the best experience on our
website. [Learn more](http://ourcodeworld.com/privacy-policy)

Got it!

[![Our Code World
Logo](How%20to%20install%20Node.js%20in%20Kali%20Linux%20|%20Our%20Code%20World_files/ocw_logo_255.png "Go to homepage")](https://ourcodeworld.com/)

Our Code World

How to install Node.js in Kali Linux
====================================

1.  [**](https://ourcodeworld.com/)
2.  [Articles](https://ourcodeworld.com/articles/)
3.  [Kali Linux](https://ourcodeworld.com/categories/kali-linux)

**Warning Javascript Disabled:** Our Code World works better with
Javascript **

How to install Node.js in Kali Linux {.text-center}
------------------------------------

-   **Published :** March 12th 2017
-   **Last modification :** March 12th 2017
-   **** 31.1K views**
-   Actions
    -   [Listen this article](javascript:void(0);)
    -   [Report article](javascript:void(0);)

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

[**E-mail](mailto:?subject=Read%20How%20to%20install%20Node.js%20in%20Kali%20Linux%20in%20Our%20Code%20World&body=https%3A%2F%2Fourcodeworld.com%2Farticles%2Fread%2F410%2Fhow-to-install-node-js-in-kali-linux)

[**Tweet](#)

[**Like](#)

1

[**+1](#)

[**Pin it](#)

[](https://twitter.com/ourcodeworld)

**

Follow Our Code World on Twitter

[](https://www.facebook.com/ourcodeworld)

**

Like Our Code World on Facebook

[](https://www.youtube.com/ourcodeworld)

**

Subscribe to our YouTube Channel

##### This could interest you

##### Become a more social person

Please enable JavaScript to view the [comments powered by
Disqus.](https://disqus.com/?ref_noscript)

##### Related articles {.card-heading .text-center}

-   [](https://ourcodeworld.com/articles/read/825/how-to-hack-an-instagram-account-with-a-dictionary-attack-using-instainsane)
    How to hack an Instagram account with a dictionary attack using
    Instainsane Kali Linux • November 18th 2018
-   [](https://ourcodeworld.com/articles/read/824/how-to-solve-kali-linux-cli-error-could-not-get-lock-var-lib-dpkg-lock-open-9-resource-temporarily-unavailable)
    How to solve Kali Linux CLI error: Could not get lock
    /var/lib/dpkg/lock – open (9: Resource temporarily unavailable) Kali
    Linux • November 12th 2018
-   [](https://ourcodeworld.com/articles/read/820/finding-an-username-across-over-75-social-networks-with-userrecon)
    Finding an username across over 75 social networks with UserRecon
    Kali Linux • November 10th 2018
-   [](https://ourcodeworld.com/articles/read/817/how-to-install-spotify-on-kali-linux)
    How to install Spotify on Kali Linux Kali Linux • October 28th 2018
-   [](https://ourcodeworld.com/articles/read/487/how-to-use-the-multiple-tabs-feature-in-the-kali-linux-terminal)
    How to use the multiple tabs feature in the Kali Linux terminal Kali
    Linux • July 2nd 2017

##### [Advertise with Our Code World](https://ourcodeworld.com/advertise-with-us) {.card-heading .text-center}

[](https://bestfreehtmlcsstemplates.com/ "Click here for more information")

**

#### Looking for new web templates?

Best Free HTML/CSS Templates

** Find the best free templates here

### Don't forget to follow us on your favorite social network {.card-title}

Enjoying this article? Follow us and don't miss any new content !

[** Follow @ourcodeworld on Twitter](https://twitter.com/ourcodeworld)
[** Like Our Code World on
Facebook](https://www.facebook.com/ourcodeworld) [** Subscribe to our
YouTube
channel](https://www.youtube.com/ourcodeworld?sub_confirmation=1) [**
Make a donation](https://www.paypal.me/ourcodeworld) [** Write for
us](https://ourcodeworld.com/write-for-us "A single person can write about everything, share something with the world now !")

#### Report article {.modal-title}

Thanks for take some of your time to report this article. Before
continue, please provide some basic information about why this article
should be reported :

​1) Reasons

Unavailable imagesIt isn't working properly or totallyIt isn't
understandable

​2) Be more specific with the problem (if you need to. max length 1000
chars)

Report

Cancel

[Carlos Delgado Our Code World © 2015 - 2019
**](https://ourcodeworld.com/about)

[Looking for a new template for your next project? Discover Best Free
HTML/CSS Templates **](https://bestfreehtmlcsstemplates.com/)

-   [Homepage](https://ourcodeworld.com/)
-   [Articles](javascript:void(0);)
    -   [All Articles](https://ourcodeworld.com/articles/)
    -   [Explore
        Categories](https://ourcodeworld.com/categories/list/categories)
-   [Android Free Apps](javascript:void(0);)
    -   [Our Code Editor](https://ourcodeworld.com/apps/our-code-editor)
-   [Projects](http://docs.ourcodeworld.com/projects)
-   [Policies](javascript:void(0);)
    -   [Comment policy](https://ourcodeworld.com/comments-policy)
    -   [Privacy policy](https://ourcodeworld.com/privacy-policy)
-   [Inquiries](javascript:void(0);)
    -   [About](https://ourcodeworld.com/about)
    -   [Advertise with us](https://ourcodeworld.com/advertise-with-us)
    -   [Contact](https://ourcodeworld.com/contact)
    -   [Write for us](https://ourcodeworld.com/write-for-us)
-   [Login](https://ourcodeworld.com/login)

**
