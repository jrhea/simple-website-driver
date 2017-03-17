# Setup

#### Download repo

```bash
  
$ git clone https://github.com/jrhea/simple-website-driver.git

```

#### Project structure

 $PROJECT_ROOT:

   
  ---  /data # contains input files to the websiteDriver.py script


  ---  /output # websiteDriver.py will output the downloaded csv file here


  ---  /src # contains source code

#### Debian/Ubuntu/Mint/etc

From $PROJECT_ROOT/src:

```bash

$ ./setup.sh

```

> NOTE: This setup script will create a $HOME/3rd-party directory to install PhantomJS

# Execution

#### How to run the script

To run existing website scripts.  Run this command from $PROJECT_ROOT/dataAquisition/src:

```bash

$ ./run.sh ../data/login.txt

```

> IMPORTANT: You can copy the format of one of the example input command files to script the download of a different file

To run in interactive mode. Run this command from $PROJECT_ROOT/src:

```bash

$ ./run.sh 

```

> NOTE: The csv file will be downloaded to: $PROJECT_ROOT/output


#### How to interact with the script

websiteDriver.py enters a command loop when it first starts up and waits
waits for the user to input a command.

```

navigate

  description: description: navigate to a url
  output: 0 if successful; otherwise, 1

getElementByXpath
  
  description: retrieve a reference to a particular html element
  output: 0 if successful; otherwise, 1

inputText

  description: enter text into the currently referenced html element
  output: 0 if successful; otherwise, 1

click

  description: click the currently referenced html element
  output: 0 if successful; otherwise, 1

waitCondition

  description: wait for an html element's text field to display a specific string
  output: 0 if successful; otherwise, 1

downloadFile

  description: monitor then download a file by constructing url path from the html element representing the filename to download
  output: 0 if successful; otherwise, 1

screenshot

  description: take a screenshot of the current state of the webpage.  Useful for debugging.
  output: 0 if successful; otherwise, 1

exit
  
  description: exit the commad loop and quit the program.

```

you must chain together commands in order to navigate the website.  for example:

Navigate to url:

```

navigate
https://www.foo.com

```

Enter username:

```

getElementByXPath
//*[@id="userId"]
2
inputText
My_Username

```

Enter password:

```

getElementByXPath
//*[@id="banner-right"]/div[1]/form/div[1]/input[2]
2
inputText
My_Password

```

Click login button:

```

getElementByXPath
//*[@id="banner-right"]/div[1]/form/div[2]/p/strong/input
2
click

```